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



