https://arxiv.org/pdf/1703.04730.pdf

ar5iv: [[1703.04730] Understanding Black-box Predictions via Influence Functions](https://ar5iv.labs.arxiv.org/html/1703.04730)

## Abstract

攻撃についても扱う



## 1 Introduction

ロバスト統計のHampel, 1974のInfluence Curveをもとにしているが、これは計算量が多いので近似している

## 2 Approach

## 2.1 Upweighting a training point 

LOOを近似し、再学習を不要にしたい

訓練データ全部を使った経験リスクに、データ点$z$についての誤差$L(z, \theta)$を重み付きで足したリスク関数で訓練したパラメータ$\hat{\theta}_{\epsilon,z}$を考える

$$
\hat{\theta}_{\epsilon,z}
:= \arg \min_{\theta} \frac{1}{N} \sum^N_{i=1} L(z_i, \theta) + \epsilon L(z, \theta)
$$

$z$を入れることによる変化分がとれるので、これの$\epsilon$での微分の$\epsilon = 0$のときの値をパラメータについての上側のinfluence functionとする

$$
\mathcal{I}_{up, params}(z) := \left . \frac{d \hat{\theta}_{\epsilon,z} }{ d \epsilon } \right | _{\epsilon = 0}
= -H^{-1}_{\hat{\theta}} \nabla_{\theta} L(z, \hat{\theta})
$$
もし$\epsilon = -\frac{1}{N}$なら

$$
\hat{\theta}_{\epsilon,z}
= \arg \min_{\theta} \frac{1}{N} \sum^N_{i=1} L(z_i, \theta) - \frac{1}{N} L(z, \theta)
$$

もし$z$が訓練データに含まれるなら、訓練データから$z$を除去した場合と同様なので、LOOの考え方を近似できる

$$
\hat{\theta}_{-z} - \hat{\theta}
\approx -\frac{1}{n} \mathcal{I}_{up, params}(z)
$$
データ点$z_{test}$におけるinfluenceを計算するため、微分の連鎖律を使う

$$
\begin{align}
\mathcal{I}_{up, loss}(z, z_{test})
:&= \left . \frac{d L(z_{test}, \hat{\theta}_{\epsilon, z}) }{ d \epsilon } \right | _{\epsilon = 0} \\
&= \nabla_{\theta} L(z_{test}, \hat{\theta})^\top
    \left . \frac{d \hat{\theta}_{\epsilon, z} }{ d \epsilon } \right | _{\epsilon = 0} \\
&= - \nabla_{\theta} L(z_{test}, \hat{\theta})^\top H^{-1}_{\hat{\theta}} \nabla_{\theta} L(z, \hat{\theta})
\end{align}
$$

## 2.2 Perturbing a training input

「もし訓練データを変えたら予測値はどう変化するか？」という反実仮想を研究することで、より緻密なinfluenceを開発できる。

訓練データ点$z=(z,y)$について、$z_{\delta} := (x+\delta, y)$を定義する

混乱（perturbation）$z\mapsto z_{\delta}$について考え、$\hat{\theta}_{z_{\delta}, -z}$を$z$を$z_{\delta}$に置き換えたときの経験リスク最小化解とする。この効果を近似するため、$z$を$z_{\delta}$に$\epsilon$で重みづけた結果得られるパラメータを
$$
\hat{\theta}_{\epsilon, z_{\delta}, -z}
:= \arg \min_{\theta \in \Theta} \frac{1}{n} \sum^n_{i=1}
L(z_i, \theta) + \epsilon L(z_{\delta}, \theta) - \epsilon L(z, \theta)
$$
と定義する。

先程と同様に計算すると
$$
\begin{align}
\left .
    \frac{d \hat{\theta}_{\epsilon, z_{\delta}, -z}}
    {d \epsilon}
\right |_{\epsilon = 0}
&= \mathcal{I}_{up, params}(z_{\delta})
- \mathcal{I}_{up, params}(z)
\\
&= - H^{-1}_{\hat{\theta}} (
    \nabla_{\theta} L(z_{\delta}, \hat{\theta})
    - \nabla_{\theta} L(z, \hat{\theta})
)
\end{align}
\tag{3}
$$
先程と同様に線形近似すると
$$
\hat{\theta}_{z_{\delta}, -z} - \hat{\theta}
\approx \frac{1}{n}
(\mathcal{I}_{up, params}(z_{\delta})- \mathcal{I}_{up, params}(z))
$$
となり、$z\mapsto z_{\delta}$の効果を閉形式で推定できる。

類似した方程式は$y$の変化にも適用される。

任意の$\delta$で近似でき、upweightingスキームは平滑化を提供するためNLPのような離散データでも扱える

もし$x$が連続で$\delta$が小さいなら、(3)をさらに近似できる

$\| \delta \| \to 0$のとき
$$
\nabla_{\theta} L(z_{\delta}, \hat{\theta})
    - \nabla_{\theta} L(z, \hat{\theta})
\approx [\nabla_x \nabla_{\theta} L(z, \hat{\theta})]\delta
$$
（数式略）

## 2.3. Relation to Euclidean distance

test pointに最も関係のあるtraining pointsを探すために、ユークリッド空間上で最近傍をみることは一般的である（e.g. Ribeiro et al. 2016）。もしすべての点が同じノルムをもつなら、最大の$x \cdot x_{test}$をもつ$x$を選ぶことと等しい（コサイン類似度的な？）。

直感のため、ロジスティック回帰を用いてそれ（ユークリッド空間での近傍）と$\mathcal{I}_{up, loss}(z, z_{test})$を比較し、influenceのほうがより正確に訓練の効果を表すことを示す.
$$
p(y|x) = \sigma(y \theta^\top x)
$$
とおき、$y\in \{-1, 1\}$で$\sigma(t) = \frac{1}{1+\exp(-t)}$とする。

training setの確率を最大化したい。
$$
L(z, \theta) = \log(1+\exp(-y \theta^\top x))\\
\nabla_{\theta} L(z, \theta) = -\sigma(-y \theta^\top x) yx\\
H_{\theta} = \frac{1}{n}\sum^n_{i=1} \sigma(\theta^\top x_i) \sigma(-\theta^\top x_i) x_i x_i^\top
$$
とすると、
$$
\mathcal{I}_{up, loss}(z, z_{test})
= - y_{test} y
\cdot \sigma(-y_{test} \theta^\top x_{test})
\cdot \sigma(-y \theta^\top x)
\cdot x_{test}^\top H^{-1}_{\hat{\theta}} x
$$
である。

$x\cdot x_{test}$との2つの重要な違いを強調しておきたい。

1. $\sigma(-y\theta^\top x)$は訓練誤差が多くてより影響の高い点をもたらし、外れ値がmodel parametersをdominateする
2. 重み付き共分散行列$H^{-1}_{\hat{\theta}}$は$z$を消したことによる他のtraining pointの「抵抗（resistance）」を測る。もし$\nabla_{\theta}L(z, \hat{\theta})$が小さな変動の方向を示すなら、その方向に動かすことは他のtraining pointsにおける誤差を顕著に増加させることはないであろうから、その影響は高くなるであろう。

Fig 1に示すように、influence functionsは最近傍よりも正確にモデルの訓練の効果を捉えている。



## 3. Efficiently calculating influence


$$
\begin{align}
\mathcal{I}_{up, loss}(z, z_{test})
= - \nabla_{\theta} L(z_{test}, \hat{\theta})^\top H^{-1}_{\hat{\theta}} \nabla_{\theta} L(z, \hat{\theta})
\end{align}
$$
を効率的に計算するにあたって2つの課題がある

1つは、経験リスクのヘシアン
$$
H_{\hat{\theta}} = \frac{1}{n} \sum^n_{i=1} \nabla_{\theta}^2 L(z_i, \hat{\theta})
$$
のformingと逆行列化である。これは$n$個のtraining pointsと$\theta \in \mathbb{R}^p$のとき$O(np^2 + p^3)$の計算量が必要になる。これはディープラーニングの数百万パラメータのモデルなどではきわめて多い。

2つ目は、すべてのtraining points $z_i$で$\mathcal{I}_{up, loss}(z_i, z_{test})$を計算しなければならないことである。

1つ目のヘシアンの問題は2次最適化においてよく研究された問題である。明示的にヘシアンを計算することを避け、代わりにHessian-vector products (HVPs）を使って効率的な近似
$$
s_{test} := H_{\hat{\theta}}^{-1} \nabla_{\theta} L(z_{test}, \hat{\theta})
$$
を行い、
$$
\mathcal{I}_{up, loss}(z, z_{test}) = - s_{test} \cdot \nabla_{\theta} L(z,\hat{\theta})
$$
を計算する。

これは2つ目の問題も解決する。$s_{test}$を事前に計算しておけば$- s_{test} \cdot \nabla_{\theta} L(z_i,\hat{\theta})$は効率的に計算できるためだ。

$s_{test}$の近似のための2つの技術について述べる。どちらも、$H_{\hat\theta}$と$[\nabla_{\theta}^2 L(z_i, \hat{\theta})]v$のHVPが任意の$v$について$\nabla_{\theta} L(z_i,\hat{\theta})$と同じ計算時間で計算可能であり、典型的には$O(p)$になるということだ。

#### Conjugate gradients (CG)

第一の技術は、行列の逆化を最適化問題に変換する標準的な技術である。
$$
H^{-1}_{\hat{\theta}} v := \arg \min_t \{ t^\top H_{\hat{\theta}} t - v^\top t \}
$$
これは$H_{\hat{\theta}} t$だけを計算すれば良く、$O(np)$である

### Stochastic estimation

標準的なCGだけでは大規模なデータセットで遅くなる可能性がある。そこで、各iterationで1サンプルだけを抽出して推定する方法がある

# 4. Validation and extensions

LOOは次の2つの仮定を置いている

1. モデルパラメータ$\hat{\theta}$は経験リスクを最小化する
2. 経験リスクは2回微分可能で厳密に凸である

influence functionsもLOOの漸近近似であるが、これらの仮定が破られた場合であっても有用な情報を提供することを示す

## 4.1. Influence functions vs. leave-one-out retraining

influence functionはtraining pointを変化させる重み$\epsilon$が無限小に小さいことを仮定する。

IFでの近似の精度をしらべるため、
$$
-\frac{1}{n} \mathcal{I}_{up, params}(z)
$$
を実際にLOO retrainingを行う
$$
L(z_{test}, \hat{\theta}_{-z}) - L(z_{test}, \hat{\theta})
$$
と比較する。10-classes MNISTとロジスティック回帰で比較しても、実測値と予測値は非常に近い（Fig2-left）

stochastic approximationも正確である（Fig2-Mid）



## 4.2. Non-convexity and non-convergence

第2節では$\hat{\theta}$を大域最小値としていた。しかし実際にはearly stoppingつきのSGDなどで推定したり、非凸の目的関数を使用することによって、得られる$\tilde{\theta}$は$\hat{\theta}$と一致しない。

その結果、$H_{\tilde{\theta}}$は負の固有値を持つ可能性がある。

その場合でもinfluence functionsは有用な結果をもたらす。

$\tilde{\theta}$の周辺で誤差の二次近似、つまり
$$
\tilde{L}(z, \theta) = L(z, \tilde\theta) 
+ \nabla L(z, \tilde \theta)^\top (\theta - \tilde\theta)
+ \frac{1}{2} (\theta - \tilde\theta)^\top
(H_{\tilde\theta} + \lambda I) (\theta - \tilde\theta)
$$
ここで$\lambda$は$H_{\tilde\theta}$が負の固有値をもつ場合に追加されるdamping termで、$L_2$正則化を追加することと対応する。

そして$\mathcal{I}_{up, loss}$を計算する

もし$\tilde\theta$が局所最適解に近い場合、結果はニュートン・ステップに相関する（Appendix B）



CNNの訓練によるnon-convexでnon-convergentにおける$\mathcal{I}_{up, loss}$の挙動を確認した。HはPD（正定値？）にならなかったのでdamping termを$\lambda = 0.01$で追加した。

それでも予実の相関係数は0.86と高い



## 4.3. Non-differentiable losses

$\nabla_{\theta}L$と$\nabla_{\theta}^2 L$が無かったらどうなるか？

微分不可能な損失でも平滑近似してinfluenceを計算できることを示す

2.3節での線形SVMはヒンジ損失の最小化をしている
$$
Hinge(s) = \max(0, 1-s)
$$
を
$$
SmoothHinge(s, t) = t \log (1 + \exp(\frac{1-s}{t}))
$$
で近似すると、平滑化度合いが高ければ予測精度は上がる（FIg３）

# 5. Use cases of influence functions



## 5.1. Understanding model behavior

2つのモデルが同じ正しい予測値を異なるやり方で出したことを示す

Inception v3 Network と RBFカーネルのSVMを使い、ImageNetから各クラスに900訓練事例を抽出したデータにおけるdog / fishの二値分類を行う。

kの方法でのNNのFreezingはCVの界隈では一般的で、ロジスティック回帰をbottleneck featuresで学習することと同値である

２つのモデル両方が正解しているtest imageを選ぶ（Fig4-top）

SVMではSmoothHinge(0.001)を使った。

#### 結果

期待通り、RBF SVMの$\mathcal{I}_{up,loss}$はピクセル距離と逆に変動し、Inceptionはpixel spaceのdistanceとは相関が非常に低かった。Fig4-Left

2つの最もhelpfulな画像（most positive -$\mathcal{I}_{up,loss}$）がFig4-Right

RBF SVMにおいてtest image近くのfish（緑の点）は大多数がhelpfulで、dogs（赤い点）は多くがharmfulで、soft nearest neighbor functionのようにRBFがふるまっていた（fig4-left）

対照的にinceptionではfishもdogもhelpfulにもharmfulにもなりうる。実際、5つ目にもっともhelpfulな訓練データはdogであった（Fig4-top）



## 5.2. Adversarial training examples

分類器は誤分類するが視覚的には判別できない画像であるadversarial test imageの先行研究はある

influence functionでadversarial training imageを作ることができる

$z_{test}$において最もlossを増やす訓練データ$z$がわかるので、adversarial versionの訓練データ点
$$
\tilde{z}_i := z_i\\
\tilde{z}_i := \Pi (\tilde{z}_i + \alpha \mathop{\text{sign}}(\mathcal{I}_{pert, loss}(\tilde{z}_i, z_{test})))
$$
のように反復的に更新する

$\alpha$はステップ幅、$\Pi$は同じ8bit表現を共有する正しい画像の集合へ射影する。この方法はadversarial test imageの方法の類推である

inception networkを使う

- 1訓練事例だけを加工して、正しく分類できていた591件のうち57%が誤分類
- 2件で77%
- 10件で590/591が誤分類



#### 複数のtestに同時に攻撃する

testのaverage lossを上げる

1つのtrainingの加工が複数のtestの予測に影響を与えた

## 5.3. Debugging domain mismatch

trainとtestの分布の不一致は予測精度を悪化させる

We show that influence functions can identifythe training examples most responsible for the errors, help-ing model developers identify domain mismatch

20Kサンプルの糖尿病患者のデータセットで10歳未満の24件のうち3件がre-admitted。そのうち20件消して4件中3件がre-admittedとすることでmismatchを人工的に作った









