[2012.15781.pdf](https://arxiv.org/pdf/2012.15781.pdf)

## Abstract

- influence-functionは知名度の割に大規模データにスケールしない
- FastIFという、シンプルにkNNで探索範囲を狭めたinfluence functionを提案
  - 80倍の高速化

## 1 Introduction

### 先行研究

- 「訓練データ点のモデルへの影響を見たい」という概念：algorithmic transparency（Lipton 2016）
- leave-one-out approach（Hastie et al., 2009）
- influence functions（Koh and Liang, 2017）

#### influence function

- 計算コストが高い：14.7M parameters * 390K dataset で2時間以上かかる（Sec 5.1）
- なぜか：

1. データ点の評価は$O(n)$
2. モデルパラメータのinverse Hessianの計算コストが高い
3. 上記の計算は並列可能であるが、先行研究のアルゴリズムでは直列

#### FastIfのアイデア

1. 全データを探索するのではなく、fast nearest neighbor search（Johnson et al., 2017）で探索範囲を狭める
   - 桁違いに計算コストを抑える
2. Hessianの推定において、品質を保ちつつ時間を半分以下にするハイパーパラメータ集合を識別
3. シンプルに並列計算へ拡張し、さらに2倍高速化

実験においてほとんどのケースで全体で2桁程度の高速化が確認された

## 2    Related Work

### Influence Functions

- seminal papers  such  as  Cook  (1977);  Cook  and  Weisberg(1980, 1982); Cook (1986). 
- Recently, Koh andLiang (2017) brought influence functions to large-scale deep learning and have been followed up by numerous publications.
  - For example, Koh et al.(2018) used them for data poisoning attacks, Schulam and Saria (2019) for calibrating trust in individual model predictions, Brunet et al. (2019) for tracing biases in word embeddings, Koh et al. (2019) and Basu et al. (2020) for identifying important groups of training data, and Feldman and Zhang(2020) for studying neural networks memorization.

#### NLPでは

- Han et al. (2020)がIFを応用
- Yang et al.(2020)はdata-augumentationで合成訓練データを評価するために活用
- Meng  et  al.  (2020)は**勾配ベースの方法**とinfluence functionを使った

#### 高速化

- Kobayashi et al.(2020) はinfluenceを高速に計算するためにinstance-specific dropout を使った

# 3 FastIF: Method Details

## 3.1    Background

$$
\DeclareMathOperator*{\argmax}{arg max\ }
\DeclareMathOperator*{\argmin}{arg min\ }
$$



- データ点$z=(x, y)$
- 誤差関数$L(z, \theta)$
- $N$訓練データ点が訓練集合$\mathcal{Z}$に含まれるとする
- 標準的な経験リスク最小化：$\hat{\theta} = \arg \min_{\theta} \frac{1}{N} \sum^N_{i=1} L(z_i, \theta)$

- 問い：訓練済みモデルパラメータ$\theta$における訓練データ点$z$がテストデータ点$z_{test}$に与えた影響
- 「モデルのふるまい」には様々な定義があるが、ここではテストデータ点のlossに焦点を当てる

### LOO

- full training set $\mathcal{Z}$と、そこから$z$を削除したデータセットで比較する

### Influence Functions

- 局所近似する
- 訓練データ点の損失を重み付ける
- そのためIFは「もし訓練データ点$z$を$\epsilon, \mathcal{I}(z, z_{test}):=\frac{dL(z_{test}, \hat{\theta}_{\epsilon,z})}{d \epsilon}$でup-weightしたときの、モデルのテストデータ点$z_{test}$の損失の変化」である
  - ここで$\hat{\theta}_{\epsilon,z}$は訓練データ点$z$において$\epsilon$でup-weightedされたモデルのパラメータ

$$
\hat{\theta}_{\epsilon,z} := \arg \min_{\theta} \frac{1}{N} \sum^N_{i=1} L(z_i, \theta) + \epsilon L(z, \theta)
$$

$\mathcal{I}(z, z_{test})$は計算量が高いため、Koh and Liang 2017では次の近似を行った
$$
\mathcal{I}(z, z_{test}) \approx
-\nabla_{\theta} L(z_{test}, \hat{\theta})^T
H^{-1}_{\hat{\theta}} \nabla_{\theta} L(z, \hat{\theta})
\tag{1}
$$
ここで$\hat{\theta}$は訓練データで訓練したモデルのオリジナルなパラメータベクトル、$H_{\hat{\theta}}$はそのヘシアン。

各訓練データ点について、通常我々は最も正の（positively）影響をもつ訓練データ点と最もネガティブな影響を持つ訓練データ点に関心がある（ポジティブあるいは「害のある（harmful）影響」とは、もし損失をup-weightingすることがテストデータ点での誤差を高めるようなデータ点のことである。ネガティブあるいは「助けになる（helpful）」は同様である）

$z_{test}$と$z$の影響値を比べることで最も正に影響のある（positively influential）、つまり最も有害な訓練データ点$z^*$を探すことができる
$$
z^* = \argmax_{z \in \mathcal{Z}} \mathcal{I}(z, z_{test})
\tag{2}
$$
arg minにすればもっともhelpfulなデータ点の探索ができる。

この近似を行ってもなお、前述のように計算コストが高い。

## 3.2    Speeding up the $\arg \max$ using $k$NN

実際には最も影響のあるデータ点に関心があるため、影響度が高い見込みのある部分集合$\hat{\mathcal{Z}}\subseteq \mathcal{Z}$に絞ることにする
$$
z^* = \argmax_{z \in \hat{\mathcal{Z}}} \mathcal{I}(z, z_{test})
\tag{3}
$$
$\hat{\mathcal{Z}}$はKhandelwal et al. (2019) と Rajani et al.(2020)にしたがって選びだした特徴量の$\ell_2$距離に基づく$z_{test}$の上位$k$近傍。

この処理は FAISS (Johnson et al., 2017)の最近傍探索ライブラリを使うと非常に高速化される。



## 3.3    Speeding up the Inverse Hessian
