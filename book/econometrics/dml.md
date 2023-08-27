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

第一項はよい挙動をし、$a \rightsquigarrow N(0, \bar{\Sigma})$となる。

$b$の項は正則化バイアス項で、一般に中心にならず発散する。first orderで以下を得る
$$
b = (E[D_i^2])^{-1}
\frac{1}{\sqrt{n}} \sum_{i\in I}
m_0(X_i)(g_0(X_i) - \hat{g}_0(X_i)) + o_P(1)
$$
ヒューリスティックには、$b$は平均がゼロにならない$m_0(X_i)(g_0(X_i) - \hat{g}_0(X_i))$の$n$個の総和で、$\sqrt{n}$で割られる。これらの項は非ゼロの平均になる。なぜなら高次元あるいは複雑な問題設定のために我々はlasso, ridge, boostingあるいはpenalized neural netsなどの正則化推定量を採用するためである。

#### （正則化バイアス）

それらの推定量において正則化は推定量の分散が爆発しないようにするものの相当なバイアスを引き起こす。とりわけ、$g_0$への$\hat{g}_0$のバイアスの収束レートは、RMSEにおいて$n^{-\phi_g}$（$\phi_g < 1/2$）である。ゆえに$b$は$D_i$が$m_0(X_i)\neq 0$で中心化されるとき$\sqrt{n} n^{-\phi_g} \to \infty$の確率的オーダーになることが期待され、よって$|\sqrt{n} (\hat{\theta}_0 - \theta_0)| \overset{p}{\to} \infty$となる