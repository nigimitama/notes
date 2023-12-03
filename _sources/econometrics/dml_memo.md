[Double/debiased machine learning for treatment and structural parameters | The Econometrics Journal | Oxford Academic](https://academic.oup.com/ectj/article/21/1/C1/5056401)

# Summary

高次元局外母数$\eta_0$があるときの低次元母数$\theta_0$のセミパラメトリック推定問題を再検討した。

古典的な問題設定との違いは、パラメータ空間を制限する伝統的な仮定（例：Donsker性）を打破するために$\eta_0$が高次元であることを許容した

$\eta_0$の推定にはMLを使う。MLにおいて過学習を防ぐための正則化はうまくいくが、ML推定量を$\theta_0$の推定のためにナイーブに接続すると、$\theta_0$の推定においては正則化バイアスと$\eta_0$の過学習が大きなバイアスを引き起こし、$N^{-1/2}$consistentにならない。

我々はパラメータ$\theta_0$の推定において正則化バイアスと過学習が2つのシンプルで重要な材料によって除去されることを示す：

1. 局外母数についてのsensitivityを削減するNeyman-orthogonal moments/scores
2. データ分割の効率的な形を提供するcross-fitting

この手法群をdouble or debiased ML (DML)と呼ぶ

我々はDMLが真のパラメータの$N^{-1/2}$近傍に集中する点推定量をもたらし、近似的に不偏で正規分布し、適切なconfidence statementsを構築可能であることを示した。

# 1. INTRODUCTION AND MOTIVATION

### motivation

例として、Robinson (1988) のpartially linear regression (PLR) model を考える
$$
Y = D\theta_0 + g_0(X) + U, \hspace{1em} E[U|X,D] = 0\\
D = m_0(X) + V, \hspace{1em} E[V|X] = 0
$$
ここで$Y$は結果変数、$D$は処置変数、$X=(X_1, \dots, X_p)$はコントロール変数、$U,V$は撹乱項である。

1つ目の式の$\theta_0$が推定したいパラメータである。もし$D$が$X$で条件付けられた下で外生であれば、$\theta_0$は処置効果パラメータとして解釈できる。

2つ目の式は交絡を追跡する、つまり処置変数のコントロール変数への依存を示す。この式それ自体は関心の対象ではないが、characterizingと正則化バイアスの除去のために重要である。多くの応用で、Xの次元数$p$は$N$より大きい。$p$は$N$を増加させていったときに消えるものではなく増加するものである。局外母数$\eta_0=(m_0, g_0)$のパラメータ空間を制限する古典的な仮定の失敗はこのためである。

### regularization bias

$\theta_0$のナイーブな推定法はMLを使うことで、例えばML推定量$D\hat{\theta}_0 + \hat{g}_0(X)$を回帰関数$D\theta_0 + g_0(X)^2$の学習に使う。

話を簡潔にするために、サンプルを2つにランダム分割するとしよう：メインパートは$n$サンプルで$i\in I$のインデックスで表し、補助パートは$N-n$として$i \in I^c$とする。単純のため$n=N/2$とする。補助パートのサンプルで$\hat{g}_0$を獲得し、$\theta_0$の推定にメインパートのサンプルを使うことにする
$$
\hat{\theta}_0 = \left( \frac{1}{n} \sum_{i\in I} D_i^2 \right)^{-1}
\frac{1}{n} \sum_{i\in I} D_i (Y_i - \hat{g}_0(X_i))
\tag{1.3}
$$


推定量$\hat{\theta}_0$は一般に$1/\sqrt{n}$より遅い収束レート、つまり
$$
|\sqrt{n} (\hat{\theta}_0 - \theta_0)| \overset{p}{\to} \infty
$$
（疑問：1/ルートnより遅いと発散するということ？）

後述するように、この「劣った」振る舞いの背後には$g_0$の学習におけるバイアスがある。

ヒューリスティックにこの$\hat{g}_0$の学習のバイアスのインパクトを説明すると、スケールされた$\hat{\theta}_0$の推定誤差は
$$
\sqrt{n} (\hat{\theta}_0 - \theta_0) =
\underbrace{
    \left( \frac{1}{n} \sum_{i\in I} D_i^2 \right)^{-1}
    \frac{1}{\sqrt{n}} \sum_{i\in I} D_i U_i
}_{:=a}
+
\underbrace{
    \left( \frac{1}{n} \sum_{i\in I} D_i^2 \right)^{-1}
    \frac{1}{\sqrt{n}} \sum_{i\in I} D_i (g_0(X_i) - \hat{g}_0(X_i))
}_{:=b}
$$
である。

第一項はよい挙動をし、$a \rightsquigarrow N(0, \bar{\Sigma})$となる。（youtubeの発表を見た感じでは近似的に従う、みたいな意味らしい）

$b$の項は正則化バイアス項で、一般に中心にならず発散する。first orderで以下を得る
$$
b = (E[D_i^2])^{-1}
\frac{1}{\sqrt{n}} \sum_{i\in I}
m_0(X_i)(g_0(X_i) - \hat{g}_0(X_i)) + o_P(1)
$$
ヒューリスティックには、$b$は平均がゼロにならない$m_0(X_i)(g_0(X_i) - \hat{g}_0(X_i))$の$n$個の総和で、$\sqrt{n}$で割られる。これらの項は非ゼロの平均になる。なぜなら高次元あるいは複雑な問題設定のために我々はlasso, ridge, boostingあるいはpenalized neural netsなどの正則化推定量を採用するためである。

#### （正則化バイアス）

それらの推定量において正則化は推定量の分散が爆発しないようにするものの相当なバイアスを引き起こす。とりわけ、$g_0$への$\hat{g}_0$のバイアスの収束レートは、RMSEにおいて$n^{-\phi_g}$（$\phi_g < 1/2$）である。ゆえに$b$は$D_i$が$m_0(X_i)\neq 0$で中心化されるとき$\sqrt{n} n^{-\phi_g} \to \infty$の確率的オーダーになることが期待され、よって$|\sqrt{n} (\hat{\theta}_0 - \theta_0)| \overset{p}{\to} \infty$となる

### 直交化による正則化バイアスの打破

直交化されたregressor $V=D-m_0(X)$を得るためにDからXの効果をpartialling outすることにより得られる直交化された式（orthogonalized formulation）を使う。具体的には
$$
\hat{V} = D - \hat{m}_0(X)
$$
ここで$\hat{m}_0$は補助的サンプル（auxiliary sample）からを用いたML推定量。

DからXの効果をpartialling out したあとは、main sampleを使って$\theta_0$のdebiased ML (DML)を構築する
$$
\check{\theta}_0 = \left( \frac{1}{n} \sum_{i\in I} \hat{V}_i D_i \right)^{-1}
\frac{1}{n} \sum_{i\in I} \hat{V}_i (Y_i - \hat{g}_0(X_i))
$$
近似的にDをXについて直交化し、$g_0$の推定値を引くことで近似的に交絡の直接効果を除去することで、$\check{\theta}_0$は(1.3)の正則化バイアスを除去している。

$\check{\theta}_0$の式は、古典的な計量経済学の文献における線形操作変数推定量と、より新しい文献におけるdebiased lassoとの直接的な繋がりを提供している。

auxiliary predictionステップの利点を説明するため、$\check{\theta}_0$の性質を述べる。スケールされた推定誤差は３つの要素に分解できる
$$
\sqrt{n}(\check{\theta}_0 - \theta_0)
= a^* + b^* + c^*
$$
$a^*$はmild conditionsのもとで以下を満たす
$$
a^* = (E[V^2])^{-1}
\frac{1}{\sqrt{n}} \sum_{i\in I} V_i U_i \rightsquigarrow N(0, \Sigma)
$$
$b^*$は$g_0, m_0$の推定における正則化バイアスの影響を捉える。具体的には
$$
b^* = (E[V^2])^{-1}
\frac{1}{\sqrt{n}} \sum_{i\in I} 
(\hat{m}_0(X_i) - m_0(X_i))
(\hat{g}_0(X_i) - g_0(X_i))
$$
で、これは$\hat{m}_0$と$\hat{g}_0$の推定誤差の積に依存する。そのため、幅広いレンジのデータ生成過程のもとで消失させることが可能である。実際、この項は$\sqrt{n}n^{-(\phi_m+\phi_g)}$で上界になり、ここで$n^{-\phi_m}, n^{-\phi_g}$はそれぞれ$\hat{m}_0, \hat{g}_0$の$m_0, g_0$への収束レートである。これは両者が比較的遅い収束レートで推定されたとしても、消失しうる。

（考察：推定誤差って本当に消失しうるのか？機械学習での予測誤差はnに大まかに依存するにしても本当に消失しうるのか疑問）

$c^* = o_P(1)$が弱い条件のもとで成り立つことを保証するにあたって、sample splittingが重要な役割を果たす。以下に概要を述べ、詳細はSection 3で述べる。

Figure 1は正則化バイアスの負のインパクトと直交化の便益を示している。ヒストグラムはcentred estimator $\hat{\theta}_0 - \theta_0$のヒストグラムで、赤い曲線はバイアスが無視可能であるという仮定のもとでの正規近似である。

### 過学習によるバイアスの除去におけるsample splittingの役割

sample splittingは$c^*$が確率的に消失するために使われる。

$c^*$は
$$
\frac{1}{\sqrt{n}} \sum_{i \in I} V_i (\hat{g}_0(X_i) - g_0(X_i))
$$
などの項を含む。この項は推定誤差と構造的未観測要因の積の和を$1/\sqrt{n}$-normalizedしたものである。

$E[V_i|X_i]=0$であることを思い出すと、この項は平均ゼロで分散は
$$
\frac{1}{n} \sum_{i \in I} (\hat{g}_0(X_i) - g_0(X_i))^2
\overset{p}{\to}
0
$$
であることがわかり、チェビシェフの不等式を使って確率的には消失することがわかる。

sample splittingの欠点は推定に使用するサンプル数が減ることによる効率性の低下である。しかし、mainとauxiliaryの2つでそれぞれ推定を行い、両者の平均を取ればfull efficiencyを取り戻す。この手続き（mainとauxiliaryの役割を取り替えて複数の推定値を取得しそれらの平均をとる）を「**cross-fitting**」と呼ぶことにする。一般にk-foldにすることもできる。Section 3で詳細を述べる。

### Neyman orthogonality and moment conditions

ML推定量
$$
\hat{\theta}_0 = \left( \frac{1}{n} \sum_{i\in I} D_i^2 \right)^{-1}
\frac{1}{n} \sum_{i\in I} D_i (Y_i - \hat{g}_0(X_i))
\tag{1.3}
$$
はモーメント条件としては
$$
\frac{1}{n} \sum_{i \in I} \varphi(W; \hat{\theta}_0, \hat{g}_0) = 0
$$
部分線形モデルにおいてはscore functionは
$$
\varphi(W; \hat{\theta}_0, \hat{g}_0) = (Y - \theta D - g(X))D
$$
この$\varphi$はgの推定に対してセンシティブであることがGateaux derivative
$$
\partial_g E[\varphi(W; \theta_0, g_0)][g - g_0] \neq 0
$$
でわかる。Section2でGateaux derivative operatorの詳細を述べる。

DML推定量
$$
\check{\theta}_0 = \left( \frac{1}{n} \sum_{i\in I} \hat{V}_i D_i \right)^{-1}
\frac{1}{n} \sum_{i\in I} \hat{V}_i (Y_i - \hat{g}_0(X_i))
$$
は
$$
\frac{1}{n} \sum_{i \in I} \psi(W; \hat{\theta}_0, \hat{\eta}_0) = 0\\
\eta = (m_0, g_0)
$$
部分線形モデルにおいては$\psi(W; \hat{\theta}_0, \hat{\eta}_0) = (Y - \alpha D - g(X))(D - m(X))$

こちらは真値において$\eta$についてのGateaux derivativeが消失する
$$
\partial_{\eta} E[\psi(W; \theta_0, \eta_0)][\eta - \eta_0] = 0
$$


### notaiton

- $Pr$：確率
- $P$：確率測度
- $W$などの大文字：ランダム要素
- $w$などの小文字：ランダム要素の固定した値
- $\|\cdot\|_{P,q}$：$L^q(P)$ノルム
  - $\|f(W)\|_{P,q}:= (\int |f(w)|^q d P(w))^{1/q}$

- $x'$：列ベクトル$x$の転置
- $\partial_{x'} f$：偏微分$(\partial / \partial x') f$



# 2. CONSTRUCTION OF NEYMAN ORTHOGONAL SCORE/MOMENTFUNCTIONS

## 2.1. Moment condition/estimating equation framework

$$
E_P[\psi(W;\theta_0, \eta_0)] = 0
$$



#### pathwise (Gateaux) derivative

$$
D_r:\tilde{T} \to \mathbb{R}^{D_\theta}
$$

$$
D_r[\eta-\eta_0]
:= \partial_r \{
    E_P[\psi(W; \theta_0, \eta_0 + r(\eta-\eta_0))]
\}
, \hspace{1em} \eta \in T
$$









