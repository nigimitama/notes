---
title: ラグランジュの未定乗数法
layout: post
date: 2020-01-30
tags: math
parmalink: /lagrange.html
---



# ラグランジュの未定乗数法

ざっくりいうと、以下の手続きで問題の制約を緩和して解く方法。

(1) 微分可能な凸関数$f(\boldsymbol{x})$に対する制約付き最小化問題があるとする。
$$
\begin{align}\min_\boldsymbol{x} \hspace{1em} & f(\boldsymbol{x})\\\text{subject to} \hspace{1em} & g(\boldsymbol{x}) \leq 0\end{align}
$$
(2) **ラグランジュ未定乗数**という未知の値$\lambda\geq0$を用いて、**ラグランジュ関数**（**ラグランジアン**）
$$
L(\boldsymbol{x}, \lambda) = f(\boldsymbol{x}) + \lambda (g(\boldsymbol{x}) - 0)=f(\boldsymbol{x}) + \lambda g(\boldsymbol{x})
$$
を作る。

(3) **ラグランジュ双対問題**
$$
\begin{align}\max_\lambda \hspace{1em} &  L(\boldsymbol{x}, \lambda)\\\text{subject to} \hspace{1em} & \lambda \geq 0\end{align}
$$
を解いていく。$L(\boldsymbol{x}, \lambda)$を$\boldsymbol{x}$で微分してゼロとおき、
$$
\boldsymbol{0} = \frac{\partial L}{\partial \boldsymbol{x}} = \frac{\partial f}{\partial \boldsymbol{x}}+ \lambda \frac{\partial g}{\partial \boldsymbol{x}}
$$
これを解いて最適解$\lambda^*, \boldsymbol{x}^*$を得る。この解$\boldsymbol{x}^*$は元の最小化問題（主問題）の解と一致することが知られている。





# 用語

## ラグランジュ緩和

以下のような最適化問題があるとする
$$
\begin{align}
\text{minimize } \hspace{1em}
& f(\boldsymbol{x})\\
\text{subject to } \hspace{1em}
& g_i(\boldsymbol{x}) = b_i \hspace{1em} (i=1,...,k)\\
& h_j(\boldsymbol{x}) \geq b_j \hspace{1em} (j=1,...,l)
\end{align}
$$
この問題の制約を緩和して、もう少し簡単な問題にするアプローチの一つがラグランジュ緩和である。

例えば等式制約$g_i(\boldsymbol{x}) = b_i$を適当な数値$\beta_i$倍して目的関数に入れる。



## ラグランジュ双対問題

微分可能な凸関数$f_i(x), (i=0,...,m)$に対する制約付き最小化問題
$$
\begin{align}\min_x \hspace{1em} & f_0(x)\\\text{subject to} \hspace{1em} & f_i(x) \leq a_i \hspace{1em} (i=1, ..., m)\end{align}
$$
のラグランジュ双対問題とは、ラグランジュ未定乗数$\lambda_i$とラグランジュ関数（ラグランジアン）
$$
L(x, \lambda) = f_0(x) + \sum^{m}_{i=1} \lambda_i (f_i(x) - a_i)
$$
を用いて、以下のように定義される。
$$
\begin{align}\max_{\lambda} \inf_{x} \hspace{1em} & L(x, \lambda)\\\text{subject to}\hspace{1em} & \lambda \geq 0\end{align}
$$



# 参考

- [ラグランジュ緩和と双対問題](http://tomomi.my.coocan.jp/text/relax1.pdf)

- 『言語処理のための機械学習入門』pp.14-19