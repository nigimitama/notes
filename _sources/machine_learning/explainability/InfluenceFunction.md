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









































