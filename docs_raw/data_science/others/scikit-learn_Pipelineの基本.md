---
title: scikit-learn Pipelineの基本の使い方
date: 2020-11-07
---



# Pipelineとは

scikit-learnには[Pipeline](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html)というclassがある。これは複数の前処理用クラスと予測モデルをまとめて一つのオブジェクトにすることができるもの。



例えば、StandardScalerで特徴量の標準化を行って線形回帰で学習/予測を行う場合、Pipelineを使わない場合は以下のようにStandardScalerとLinearRegressionで別々にfitやtransformを行わないといけない。

```python
# データの用意
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
X, y = make_regression(random_state=0)
X_train, X_test, y_train, y_test = \
    train_test_split(X, y, random_state=0)
    
# Pipelineを使わない場合
scaler = StandardScaler()
estimator = LinearRegression()
## fit
X_train_ = scaler.fit_transform(X_train)
estimator.fit(X_train_, y_train)
## predict
X_test_ = scaler.transform(X_test)
y_pred = estimator.predict(X_test_)
```

この処理を実際のアプリにデプロイすることを考えると、fit済みのscalerとestimatorをそれぞれ保存・管理してアプリ上に展開しないといけない。

今回はscalerが一つなのでまだいいが、これが数十個になると**非常に面倒**であり、そうした複雑なコードは**バグのもと**になる。

一方、Pipelineを使えば同様の処理は以下のように書くことができる。

```python
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
X, y = make_regression(random_state=0)
X_train, X_test, y_train, y_test = \
    train_test_split(X, y, random_state=0)

# pipelineを使う場合
pipe = Pipeline(steps=[
    ('scaler', StandardScaler()),
    ('estimator', LinearRegression())
])
pipe.fit(X_train, y_train)
y_pred_ = pipe.predict(X_test)
```

```python
# もちろん同じ結果が得られる
all(y_pred == y_pred_)  # True
```



# 自作のTransformerを作る

自作の前処理用クラスを作るにはどうしたらよいのだろうか。



## 基底クラスを定義する

StandardScalerなどの[ソースコード](https://github.com/scikit-learn/scikit-learn/blob/0fb307bf3/sklearn/preprocessing/_data.py#L517)を見ると

```python
class StandardScaler(TransformerMixin, BaseEstimator):
    ...
```

というようにTransformerMixin, BaseEstimatorを継承している。

[TransformerMixin](https://github.com/scikit-learn/scikit-learn/blob/0fb307bf39bbdacd6ed713c00724f8f871d60370/sklearn/base.py#L660)は`fit_transform`しかメソッドを持っていない一方、Transformerは`fit`と`transform`も持たないといけないので、そちらは自分で定義してやる必要がある。

なので[この記事](https://qiita.com/kazetof/items/fcfabfc3d737a8ff8668)に書いてあるように

```python
from sklearn.base import BaseEstimator, TransformerMixin

class BaseTransformer(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return self
```

のようなクラスを定義してやれば使いやすい基底クラスになるはず。



## 自作のTransformerを定義する

上で定義した基底クラスを継承して、やりたい処理を書けば自作のTransformerの完成。

```python
class Double(BaseTransformer):
    
    def transform(self, X):
        return X*2

```



## 例

データの生成からPipelineでの利用まで全体をコードに書くなら、以下のような感じ。

```python
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin

class BaseTransformer(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return self


class Double(BaseTransformer):
    
    def transform(self, X):
        return X*2

    
X, y = make_regression(random_state=0)
X_train, X_test, y_train, y_test = \
    train_test_split(X, y, random_state=0)

# pipelineを使う場合
pipe = Pipeline(steps=[
    ('double', Double()),
    ('estimator', LinearRegression())
])
pipe.fit(X_train, y_train)
pipe.predict(X_test)
```



# memory：fitの再計算を回避する

transformerのfitに多くの計算量を要する場合、fitしたtransformerをキャッシュすることができる。引数`memory`にディレクトリのパスの文字列かjoblib.Memoryオブジェクトを入れることで、そちらにキャッシュされる。

[6.1.1.3. Caching transformers: avoid repeated computation](https://scikit-learn.org/stable/modules/compose.html#caching-transformers-avoid-repeated-computation)

```python
from tempfile import mkdtemp
from shutil import rmtree
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
estimators = [('reduce_dim', PCA()), ('clf', SVC())]
cachedir = mkdtemp()
pipe = Pipeline(estimators, memory=cachedir)

# Clear the cache directory when you don't need it anymore
rmtree(cachedir)
```



# 参考

[sklearn.pipeline.Pipeline — scikit-learn 0.23.2 documentation](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html)

[6.1. Pipelines and composite estimators — scikit-learn 0.23.2 documentation](https://scikit-learn.org/stable/modules/compose.html#pipeline)

[sklearnのpipelineに自分で定義した関数を流し込む - Qiita](https://qiita.com/kazetof/items/fcfabfc3d737a8ff8668)