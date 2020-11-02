---
title: データの前処理で並列処理を使う
date: 2020-10-01
---



pythonのmultiprocessingパッケージについてのメモ。





# コード例

こう書けば良いんじゃないかな、と思った実装例を載せていきます。

以下では説明の簡単のために'x'というカラムを2倍にするだけのdoubleという関数を並列処理にしていますが、実際にはWeb APIを呼び出すときに使ったりします。



## ProcessクラスとPipeクラスを使う場合

処理するデータを明示的に分割して別々のプロセスで処理する場合。

```python
import pandas as pd
from multiprocessing import Process, Pipe


def double(conn) -> None:
    '''親プロセスからデータを受け取って処理して送り返す'''
    records = conn.recv()
    records = map(_double, records)
    conn.send(records)
    conn.close()
    return None


def _double(record: dict) -> dict:
    '''xというカラムを2倍にする'''
    record['x'] = record['x'] * 2
    return record


def multipocess(df: pd.DataFrame, n_workers: int) -> pd.DataFrame:
    # DataFrameを送ることはできないのでdictのListにする
    records = df.to_dict('records')

    # データを分割
    size = len(records) // n_workers + 1
    records_list = _each_slice(records, size)

    parent_conns = [None] * n_workers
    child_conns = [None] * n_workers
    processes = [None] * n_workers
    for i in range(n_workers):
        # 子プロセスにデータを送るためのPipeを作成
        parent_conns[i], child_conns[i] = Pipe()
        # 子プロセスを作成
        processes[i] = Process(
            target=double,
            args=(child_conns[i],)
        )
        # 子プロセスにデータを送る
        parent_conns[i].send(records_list[i])
        # 子プロセスの処理を開始
        processes[i].start()

    results = [None] * n_workers
    for i in range(n_workers):
        # 子プロセスから結果を受け取り
        results[i] = parent_conns[i].recv()
        # 子プロセスをjoin
        processes[i].join(timeout=10)

    df_list = [pd.DataFrame(res) for res in results]
    return pd.concat(df_list).reset_index(drop=True)


def _each_slice(arr: list, size: int) -> list:
    '''listを要素数sizeのリストに分割する'''
    return [arr[i:i + size] for i in range(0, len(arr), size)]


if __name__ == '__main__':
    # データを用意
    df = pd.DataFrame({'x': list(range(10))})
    # 並列処理
    df = multipocess(df, n_workers=4)
    print(df)

```

結果

```
    x
0   0
1   2
2   4
3   6
4   8
5  10
6  12
7  14
8  16
9  18
```





## Poolクラスを使う場合

データを分けて複数のプロセスを管理して‥という作業をPoolクラスに任せる場合。

こっちのほうが楽です。

ただ、使えない環境もあります。AWS Lambdaではプロセスの共有メモリがサポートされていないのでPoolクラスはエラーを起こします。その場合は面倒ですが前節のPipeクラスを使う必要があります[^1]。

```python
import pandas as pd
from multiprocessing import Pool


def double(record: dict) -> dict:
    record['x'] = record['x'] * 2
    return record


if __name__ == '__main__':
    # データを用意
    df = pd.DataFrame({'x': list(range(10))})
    # DataFrameを送ることはできないのでdictのListにする
    records = df.to_dict('records')

    # 並列処理
    n_workers = 4
    with Pool(n_workers) as pool:
        results = pool.map(double, records)

    df = pd.DataFrame(results)
    print(df)

```

結果

```
    x
0   0
1   2
2   4
3   6
4   8
5  10
6  12
7  14
8  16
9  18
```





# なぜmultiprocessingなのか

ちなみに、なぜmultiprocessingなのかというと、pandasがmultithreadに非対応なので[^2]、並列処理する関数の中でpandasも使えるという実装の自由度を考えるとデータ処理で使うにはmultiprocessingのほうが相性が良いのかなと思っています。pandasを使わないのであればmultithreadでいいかもしれません。





[^1]: [Parallel Processing in Python with AWS Lambda | AWS Compute Blog](https://aws.amazon.com/jp/blogs/compute/parallel-processing-in-python-with-aws-lambda/)

[^2]: [Frequently Asked Questions (FAQ) — pandas 1.1.3 documentation](https://pandas.pydata.org/pandas-docs/stable/user_guide/gotchas.html#thread-safety)。ここではver.0.11の話をしていますが、私は0.25.3時代に実際にmultithreadを試して上手く行かなかった経験があります。おそらく1.1.3現在も変わらないはず。
