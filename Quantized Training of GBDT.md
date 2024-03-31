https://arxiv.org/pdf/2207.09682.pdf

## Introduction

Neural Networkではlow-precision training（quantization）が標準的になってきている

分散学習においてもhigh-precision floating pointはコミュニケーションコストになっている

この論文ではGBDTのためのlow-precision training algorithmを提案。これは確率的勾配量子化（stochastic gradient quantization）をベースとしている。**各決定木を訓練する前に、勾配を低精度（2-bitか3-bit）に量子化する。**それにより、大部分のFloating Pointの演算を整数の演算に置き換えることができ、

- 計算時間を短縮
- メモリ使用量を減らす
- キャッシュの活用を改善

することができる。

また、予測精度を保つため、

- 勾配量子化における確率的丸めこみ（stochastic rounding）
- 元の勾配による葉のrefit（leaf-value refitting with original gradient values）

の技術も提案される。

（→　originalでrefitするということはモデルサイズは変わらずか？）

GBDTの分散学習は勾配統計量の同期に基づく。勾配統計量は各特徴量のヒストグラムに要約される。量子化された勾配を使えば整数のhistogram valuesだけが必要になる。コミュニケーションコストは小さくなる。

SOTAのGBDTツールたち（XGBoost, CatBoost）と比べて2倍のスピードアップを達成した

## Related Work

NNet

RatBoostはboostingにおけるサンプルの重みに量子化を用いた。

GBDTのfederated learningの文脈で、FPを整数（53-bit interger）にする研究はあった

BitBoostは訓練の高速化のために量子化勾配を利用（ただし決定論的な方法で使っている。本研究では確率的に使う）

## 3    Preliminaries of GBDT Algorithms

各iterationでは現状の予測値に基づくGradientとHessianが計算され、そして決定木が負のGradientにfitされる。

$k+1$回目の反復において、現状のサンプル$i$の予測値を$\hat{y}_i^k$とすると、誤差関数$l$のgradientとhessianは
$$
g_i=\frac{\partial l\left(\hat{y}_i^k, y_i\right)}{\partial \hat{y}_i^k},
\quad
h_i=\frac{\partial^2 l\left(\hat{y}_i^k, y_i\right)}{\left(\partial \hat{y}_i^k\right)^2}
$$
となる。

葉$s$について、葉に含まれるデータの番号（index）の集合を$I_s$とする。葉$s$における$g_i$と$h_i$のサンプルについての合計を
$$
G_s = \sum_{i\in I_s} g_i,
\quad
H_s = \sum_{i\in I_s} h_i
$$
とする。反復$k+1$回目において、木構造が固定されたものとすると、訓練誤差は二次のテイラー近似で
$$
\mathcal{L}_{k+1} \approx \mathcal{C}+\sum_s\left(\frac{1}{2} H_s w_s^2+G_s w_s\right)
$$
ここで$\mathcal{C}$は定数で、$w_s$は葉$s$の予測値である。近似誤差の最小化により最適値が得られる
$$
w_s^*=-\frac{G_s}{H_s}, \quad \mathcal{L}_s^*=-\frac{1}{2} \cdot \frac{G_s^2}{H_s}
$$
最適な木構造を探すのは困難であるため、木は貪欲かつ反復的に訓練される。

葉$s$を2つの子$s_1, s_2$に分割するとき、近似損失の減少分は次のように計算できる。
$$
\Delta \mathcal{L}_{s \rightarrow s_1, s_2}=\mathcal{L}_s^*-\mathcal{L}_{s_1}^*-\mathcal{L}_{s_2}^*=\frac{G_{s_1}^2}{2 H_{s_1}}+\frac{G_{s_2}^2}{2 H_{s_2}}-\frac{G_s^2}{2 H_s}
$$
葉$s$にとっての最適な分割条件の探索は、すべての特徴のすべての分割候補点を数え上げて、最も損失の減少が多いものが選ばれる。

最適分割点の探索を高速化するために用いられるのはヒストグラムである。histogram based GBDTの基本的なアイデアは特徴量の値をbinsに分割する。histogramのbinsは、そのbinに含まれるデータのgradientsとhessiansの総和が記録されている。binsの境界値のみが分割候補点になる。

> Algorithm 1 Histogram Construction for Leaf $s$
> Input: Gradients $\left\{g_1, \ldots, g_N\right\}$, Hessians $\left\{h_1, \ldots, h_N\right\}$
> Input: Bin data data $[N][J]$, Data indices in leaf $s$ denoted by $I_s$
> Output: Histogram ${hist}_s$
> for $i \in I_s, j \in\{1 \ldots J\}$ do
>     bin $\leftarrow \operatorname{data}[i][j]$
>     $hist_s[j][bin] . g \leftarrow$  $hist_s[j][$ bin $] . g+g_i$
>     $hist_s[j][b i n] . h \leftarrow$  $hist_s[j][b i n] . h+h_i$
> end for

伝統的には$g_i$と$h_i$には32-bit floating point numbersが使われ、histogramへの累計には32-bitか64-bitのFPが必要になる。

次節で我々は$g_i, h_i$をどのように量子化して計算コストを抑えるのかを示す。



## 4    Quantized Training of GBDT

### 4.1 Framework for Quantized Training

まず$g_i$と$h_i$を低ビット幅（low-bitwidth）の整数$\tilde{g}_i, \tilde{h}_i$に量子化する。

すべての訓練サンプルの$g_i$と$h_i$のレンジを、等しい長さの区間へと分割する。$B$-bit $(B \geq 2)$ 整数の勾配を使うために、$2^B - 2$個の区間を使う。各区間の最後は整数値と対応するため、全体で$2^B - 1$個の整数値になる。

1次の導関数$g_i$は正の値も負の値もとるため、半分の区間は負の値のために割り当てられ、残り半分は正の値に割り当てられる。

2次の導関数$h_i$は一般的にGBDTで使われる誤差関数のほとんどすべてが非負の値をもつため、以下の議論では$h_i \geq 0$と仮定する。

それゆえ、区間の長さは$g_i, h_i$それぞれに対して
$$
\delta_g=\frac{\max _{i \in[N]}\left|g_i\right|}{2^{B-1}-1},
\quad
\delta_h=\frac{\max _{i \in[N]} h_i}{2^B-2}
$$
となる。これにより、低ビット幅の勾配は
$$
\tilde{g}_i=\operatorname{Round}\left(\frac{g_i}{\delta_g}\right),
\quad
\tilde{h}_i=\text { Round }\left(\frac{h_i}{\delta_h}\right)
$$
で計算できる。ここで$\text{Round}()$は浮動小数点数を定数に丸める関数である。

なお、もし$h_i$が定数なら、量子化する必要はない。

詳細なrounding strategyは4.2節に書く。

Algorithm 1の$g_i, h_i$を$\tilde{g}_i, \tilde{h}_i$に置き換える。もとの勾配の和の計算は整数の和の計算に置き換えられ、histogram binsの統計量$g$と$h$は整数になる。

分岐による損失の減少分

$$
\Delta \mathcal{L}_{s \rightarrow s_1, s_2}=\mathcal{L}_s^*-\mathcal{L}_{s_1}^*-\mathcal{L}_{s_2}^*=\frac{G_{s_1}^2}{2 H_{s_1}}+\frac{G_{s_2}^2}{2 H_{s_2}}-\frac{G_s^2}{2 H_s}
$$

の$G_{s_1}, H_{s_1}, G_{s_2}, H_{s_2}$は整数の$\widetilde{G}_{s_1}, \widetilde{H}_{s_1}, \widetilde{G}_{s_2}, \widetilde{H}_{s_2}$に置き換えられる。

我々は2から4bitの量子化された勾配が十分よい精度をもたらすことを発見した。また、6.1節と7.4.3節で議論するが、ヒストグラムにおける累積した低ビット幅の勾配には16bit整数で十分であった。それゆえ、大部分の演算は低ビット幅の整数によって行われる。浮動小数点数の演算が必要になるのは本来の勾配とヘシアンとsplit gainを計算するときだけである。とくに、split gainは

$$
\Delta \widetilde{\mathcal{L}}_{s \rightarrow s_1, s_2}
=
\frac{ \left(\widetilde{G}_{s_1} \delta_g\right)^2}{2 \widetilde{H}_{s_1} \delta_h}
+\frac{\left(\widetilde{G}_{s_2} \delta_g\right)^2}{2 \widetilde{H}_{s_2} \delta_h}
-\frac{\left(\widetilde{G}_s \delta_g\right)^2}{2 \widetilde{H}_s \delta_h}
$$

と推定される。ここで勾配の統計量のスケールは$\delta_g$と$\delta_h$を乗じることで復元される。

Figure 1は量子化されたGBDTのワークフローを要約している。



### 4.2 Rounding Strategies and Leaf-Value Refitting

我々はrounding戦略が精度に顕著な影響を与えることを発見した。最接近整数丸め（rounding to the nearest integer number）は合理的な選択に見える。しかし、この戦略では精度が大幅に低下することがわかった。代わりに確率的なrounding戦略（stochastic rounding strategy）を採用する。$\mathbb{E}[\widetilde{g}_i]=g_i / \delta_g$であるような値$\tilde{g}_i$がランダムな値$\lfloor g_i / \delta_g\rfloor$か$\lceil g_i / \delta_g\rceil$をとるとする。

round-to-nearest $RN$の正式な定義は以下のようになる
$$
\operatorname{RN}(x)= \begin{cases}\lfloor x\rfloor, & x<\lfloor x\rfloor+\frac{1}{2} \\
\lceil x\rceil, & x \geq\lfloor x\rfloor+\frac{1}{2}\end{cases}
$$
確率的な丸め込み$SR$は
$$
\operatorname{SR}(x)=\left\{\begin{array}{lll}
\lfloor x\rfloor, & \text { w.p. } & \lceil x\rceil-x \\
\lceil x\rceil, & \text { w.p. } & x-\lfloor x\rfloor
\end{array}\right.
$$
となる（$\text{w.p.}$はおそらくwith probabilityの意味）。

split gainは勾配の総和で計算されるため、確率的な丸め込みは総和への不偏推定量となる、すなわち
$$
\mathbb{E}[\widetilde{G} \delta_g]=G,
\quad 
\mathbb{E}[\widetilde{H} \delta_h] = H
$$
である。

確率的な丸め込みの重要性はニューラルネットの量子化学習[13]とDimBoost[16]のヒストグラム分解でも認識されている。

確率的な丸め込みにより、split gain推定の誤差は高い確率で小さい値に制限されるというsection 5の定理が提供できる。

量子化された勾配により、最適なleaf valueは
$$
\widetilde{w}_s^*=-\frac{\widetilde{G}_s \delta_g}{\widetilde{H}_s \delta_h}
$$
となり、多くのケースで$\widetilde{w}_s^*$は良い結果をもたらすのに十分である。

しかし、ランキングなど一部の損失関数では、木の成長が止まったあとに元の勾配でleaf valueをrefittingする方法が精度を向上させることがわかった。BitBoost [8] も同様の方法をとっているが、BitBoostと違い、本手法はsplit gainのヘシアンを木の成長中も考慮するがBitBoostではヘシアンを定数として扱い真のヘシアンをleaf valueのrefittingのときだけ使う。

