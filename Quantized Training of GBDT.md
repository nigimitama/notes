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



