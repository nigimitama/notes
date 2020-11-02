---
title: バイアスとバリアンス
date: 2020-06-10
---



# 回帰の場合



特徴量ベクトルを$X$とし、目的変数は$Y=f(X) + \varepsilon$であると仮定する。

$f(X)$は$Y$の予測可能な部分で、$\varepsilon$は予測不能なノイズで、$\text{E}[\varepsilon]=0,\ \text{Var}[\varepsilon]=\sigma^2_{\varepsilon}$とする。

議論を簡潔にするため、データにおける$x_i$の値は決定論的に決められているとする。

学習データセット$\mathcal{D}$で学習した予測器を$\hat{f}(x; \mathcal D)$とする。

様々な学習データセット$\mathcal D$にわたっての期待値をとる操作を${\rm E}_{\mathcal D}$と表す。



平均2乗誤差の下での、$X=x_0$における期待予測誤差（expected prediction error）もしくは汎化誤差（generalization error）と呼ばれるものは、
$$
{\rm EPE} (x_0) = {\rm E}_{\mathcal D}[(Y - \hat{f}(x_0; \mathcal D))^2 | X = x_0]
$$

これを分解すると
$$
\begin{align}
\text{EPE}(x_0)&=\text{E}_{\mathcal D}[(Y-\hat{f}(x_0; \mathcal{D}))^2|X=x_0]\\
&= \sigma^2_{\varepsilon} + (\text{E}_{\mathcal D}[\hat{f}(x_0; \mathcal{D})]
- f(x_0))^2+ \text{E}_{\mathcal D}[(\hat{f}(x_0; \mathcal{D}) - \text{E}_{\mathcal D}[\hat{f}(x_0; \mathcal{D})])^2]\\
&= \sigma^2_{\varepsilon} + \text{Bias}(\hat{f}(x_0; \mathcal{D}))^2 + \text{Var}_{\mathcal D}(\hat{f}(x_0; \mathcal{D}))\\
&= \text{削減不能な誤差} + \text{バイアス}^2 + \text{バリアンス（分散）}
\end{align}
$$
と分解できることが知られている。



## 展開

この分解の過程を以下で整理していく。ただし、記号を以下のように簡略化する
$$
\begin{align}
f &:= f(x_0)\\
\hat{f} &:= \hat{f}(x_0; \mathcal{D})\\
{\rm E} &:= {\rm E}_{\mathcal D}\\
{\rm Var} &:= {\rm Var}_{\mathcal D}\\
\end{align}
$$

$$
\begin{align}
\text{EPE}(x_0)
&=\text{E}[(Y-\hat{f})^2]\\
&={\rm E}[(Y - {\rm E}[\hat{f}] + {\rm E}[\hat{f}] - \hat{f})^2]\\
&={\rm E}[(Y - {\rm E}[\hat{f}])^2 
+ 2(Y - {\rm E}[\hat{f}])({\rm E}[\hat{f}] - \hat{f}) 
+ ({\rm E}[\hat{f}] - \hat{f})^2]\\
&={\rm E}[(Y - {\rm E}[\hat{f}])^2]
+ {\rm E}[2(Y - {\rm E}[\hat{f}])({\rm E}[\hat{f}] - \hat{f})]
+ {\rm E}[({\rm E}[\hat{f}] - \hat{f})^2] \tag{1}
\end{align}
$$

ここで式$(1$)の第1項は
$$
\begin{align}
&{\rm E}[(Y - {\rm E}[\hat{f}])^2]\\
&= {\rm E}[Y^2 - 2Y{\rm E}[\hat{f}] + {\rm E}[\hat{f}]^2]\\
&= {\rm E}[(f+\varepsilon)^2 - 2(f + \varepsilon){\rm E}[\hat{f}]
+ {\rm E}[\hat{f}]^2]\\
&={\rm E}[
(f^2 + 2f\varepsilon + \varepsilon^2)
- (2f{\rm E}[\hat{f}] + 2\varepsilon{\rm E}[\hat{f}])
- {\rm E}[\hat{f}]^2
]\tag{2}
\end{align}
$$
と分解でき、ここで${\rm E}[\varepsilon]=0$と期待値の線形性$c{\rm E}[X] = {\rm E}[cX]$から、$\varepsilon$が含まれる項はゼロが掛かってゼロになるので式$(2)$は
$$
\begin{align}
&{\rm E}[
(f^2 + 2f\varepsilon + \varepsilon^2)
- (2f{\rm E}[\hat{f}] + 2\varepsilon{\rm E}[\hat{f}])
+ {\rm E}[\hat{f}]^2
]\tag{2}\\
&= 
{\rm E}[\varepsilon^2]
+ {\rm E}[f^2 - 2f{\rm E}[\hat{f}] +{\rm E}[\hat{f}]^2]\\
&= {\rm E}[\varepsilon^2]
+ {\rm E}[(f - {\rm E}[\hat{f}])^2]
\end{align}
$$
である。

式$(1)$の第2項は、${\rm E}[\hat{f}]$が定数であることと、期待値と定数の関係${\rm E}[X - c] = {\rm E}[X]-c$から、
$$
{\rm E}[{\rm E}[\hat{f}] - \hat{f}]
= {\rm E}[\hat{f}] - {\rm E}[\hat{f}] = 0
$$
であるので、第2項はゼロになる。

ゆえに式$(1)$は
$$
\begin{align}
&{\rm E}[(Y - {\rm E}[\hat{f}])^2]
+ {\rm E}[2(Y - {\rm E}[\hat{f}])({\rm E}[\hat{f}] - \hat{f})]
+ {\rm E}[({\rm E}[\hat{f}] - \hat{f})^2] \tag{1}\\
&= {\rm E}[\varepsilon^2] 
+ {\rm E}[(f - {\rm E}[\hat{f}])^2]
+ {\rm E}[({\rm E}[\hat{f}] - \hat{f})^2]\tag{3}
\end{align}
$$
となる。

式$(3)$の第1項は、
$$
\begin{align}
{\rm Var}[\varepsilon]
&= {\rm E}[(\varepsilon - {\rm E}[\varepsilon])^2]\\
&= {\rm E}[\varepsilon^2 -2\varepsilon {\rm E}[\varepsilon] + {\rm E}[\varepsilon]^2]\\
&= {\rm E}[\varepsilon^2 -2\varepsilon \cdot 0 + 0^2]\\
&= {\rm E}[\varepsilon^2]
\end{align}
$$
なので、ノイズ$\varepsilon$の分散に等しい。

式$(3)$の第2項は、$f$と${\rm E}[\hat{f}]$が定数であるため
$$
\begin{align}
&{\rm E}[(f - {\rm E}[\hat{f}])^2]\\
&=(f - {\rm E}[\hat{f}])^2\\
\end{align}
$$
で、これは真の関数$f$と予測値の期待値${\rm E}[\hat{f}]$の差（バイアス）の2乗である。

式$(3)$の第3項は、予測値$\hat{f}$の分散（バリアンス）である。

よって、
$$
\begin{align}
& {\rm E}[\varepsilon^2] 
+ {\rm E}[(f - {\rm E}[\hat{f}])^2]
+ {\rm E}[({\rm E}[\hat{f}] - \hat{f})^2]\tag{3}\\
&= \sigma_\varepsilon^2
+ (f - {\rm E}[\hat{f}])^2
+ {\rm E}[({\rm E}[\hat{f}] - \hat{f})^2]\\
&= \sigma^2_{\varepsilon} + \text{Bias}(\hat{f})^2 + \text{Var}(\hat{f})\\
&= \text{削減不能な誤差} + \text{バイアス}^2 + \text{バリアンス（分散）}
\end{align}
$$
である。

まとめると
$$
\begin{align}\text{EPE}(x_0)&=\text{E}[(Y-\hat{f})^2]\\&={\rm E}[(Y - {\rm E}[\hat{f}] + {\rm E}[\hat{f}] - \hat{f})^2]\\&={\rm E}[(Y - {\rm E}[\hat{f}])^2 + 2(Y - {\rm E}[\hat{f}])({\rm E}[\hat{f}] - \hat{f}) + ({\rm E}[\hat{f}] - \hat{f})^2]\\&={\rm E}[(Y - {\rm E}[\hat{f}])^2]+ {\rm E}[2(Y - {\rm E}[\hat{f}])({\rm E}[\hat{f}] - \hat{f})]+ {\rm E}[({\rm E}[\hat{f}] - \hat{f})^2] \tag{1}\\&={\rm E}[(Y - {\rm E}[\hat{f}])^2]+ 2(Y - {\rm E}[\hat{f}])\underbrace{{\rm E}[({\rm E}[\hat{f}] - \hat{f})]}_{=0}+ {\rm E}[({\rm E}[\hat{f}]- \hat{f})^2]\\&= {\rm E}[\varepsilon^2] + {\rm E}[(f - {\rm E}[\hat{f}])^2]+ {\rm E}[({\rm E}[\hat{f}] - \hat{f})^2]\tag{3}\\&= \sigma_\varepsilon^2+ (f - {\rm E}[\hat{f}])^2+ {\rm E}[({\rm E}[\hat{f}] - \hat{f})^2]\\&= \sigma^2_{\varepsilon} + \text{Bias}(\hat{f})^2 + \text{Var}(\hat{f})\\&= \text{削減不能な誤差} + \text{バイアス}^2 + \text{バリアンス（分散）}\\\end{align}
$$
である。



## バイアス、バリアンスの意味

### 削減不能な誤差（irreducible error）

$$
{\rm Var}_{\mathcal D}[\varepsilon] = \sigma^2_{\varepsilon}
$$

$Y$の分散であり、ノイズの分散。

データの測定誤差などに由来する。

削減できないので、予測誤差のバイアスーバリアンス分解を議論するときに、この項を省くために、$Y$と$\hat{f}$の誤差ではなく$f$と$\hat{f}$の誤差を分解して
$$
\begin{align}
&{\rm E}[(f - \hat{f})^2]\\
&= {\rm E}[(f - {\rm E}[\hat{f}] + {\rm E}[\hat{f}] - \hat{f})^2]\\
&= {\rm E}[(f - {\rm E}[\hat{f}])^2]
+ 2(f - {\rm E}[\hat{f}])
\underbrace{{\rm E}[({\rm E}[\hat{f}] - \hat{f})]}_{0}
+ {\rm E}[({\rm E}[\hat{f}] - \hat{f})^2]\\
&= (f - {\rm E}[\hat{f}])^2
+ {\rm E}[({\rm E}[\hat{f}] - \hat{f})^2]\\
&= {\rm Bias}(\hat{f})^2 + {\rm Var}(\hat{f})
\end{align}
$$
とする場合もある。



### バイアス（Bias）

$$
\text{Bias}(\hat{f}(x_0; \mathcal{D}))
= \text{E}_{\mathcal D}[\hat{f}(x_0; \mathcal{D})]- f(x_0)
$$



予測値の平均と真の値との差。

多くの場合、より複雑なモデルを用いて予測すると、それだけバイアスは減少し、代わりにバリアンスが増加する。

### バリアンス（Variance）

$$
\text{Var}_{\mathcal D}(\hat{f}(x_0; \mathcal{D}))
= \text{E}_{\mathcal D}[(\hat{f}(x_0; \mathcal{D}) - \text{E}_{\mathcal D}[\hat{f}(x_0; \mathcal{D})])^2]
$$

（学習データセットを変えていったときの）予測値の分散。

学習データセットを変えるたびに予測値がばらつく、ということは、学習・予測の安定性が低いということ。すなわち、単一の学習データセットに過学習していることに由来すると考えられる。



## 参考

- [Hastie, T., Tibshirani, R., & Friedman, J. (2009). The elements of statistical learning: data mining, inference, and prediction. Springer Science & Business Media.](https://web.stanford.edu/~hastie/Papers/ESLII.pdf)
- [Geman, S., Bienenstock, E., & Doursat, R. (1992). Neural networks and the bias/variance dilemma. *Neural computation*, *4*(1), 1-58.](http://delta-apache-vm.cs.tau.ac.il/~nin/Courses/NC06/VarbiasBiasGeman.pdf)





# 分類の場合

いつか書く



## 参考

- [Tibshirani, R. (1996). *Bias, variance and prediction error for classification rules*. University of Toronto, Department of Statistics.](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.38.4282&rep=rep1&type=pdf)

- [Breiman, L. (1996). *Bias, variance, and arcing classifiers*. Tech. Rep. 460, Statistics Department, University of California, Berkeley, CA, USA.](https://www.stat.berkeley.edu/~breiman/arcall96.pdf)

- Kohavi, R. and Wolpert, D.H.[1996] Bias Plus Variance Decomposition for Zero-One Loss Functions, ftp starry.stanford.edu/pub/ronnyk/biasVar.ps

