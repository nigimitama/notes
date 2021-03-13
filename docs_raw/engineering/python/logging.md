---
title: loggingの使い方メモ
---



# 基本的な使い方

（[Logging HOWTO — Python 3.9.1 ドキュメント](https://docs.python.org/ja/3/howto/logging.html#configuring-logging)のコードを参考にしている）

```python
import logging

# loggerを作成する
logger = logging.getLogger('simple_example')
"""
NOTE: getLoggerのnameが同じであれば、同じloggerを参照する

Example
-------
>>> logger = logging.getLogger('simple_example')
>>> logger2 = logging.getLogger('simple_example')
>>> id(logger) == id(logger2)
True
"""

logger.setLevel(logging.DEBUG)

# コンソールに出力するためにStreamHandlerを設定する
# （ファイルに出力するときはFileHandlerを同様に設定する）
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# Handlerの出力のフォーマットを設定する
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# StreamHandlerのインスタンスをloggerに設定する
logger.addHandler(ch)

# ログメッセージを出すときは以下のように行う
logger.debug('debug message')
logger.info('info message')
logger.warning('warn message')
logger.error('error message')
logger.critical('critical message')
```



# loggerを作る関数を自作する

上記のようなログの設定を毎度やるのは面倒なので関数にしたい

その際、単純に上の処理を関数にまとめると、その関数が複数回呼ばれて同じ名前のloggerが複数回参照された場合はそのたびに毎回`addHandler`で`StreamHandler`を設定してしまうため、ログ出力が重複する。

そこで`hasHandlers`を使って、Handlerがなければ追加するようにするとよい。

```python
import logging


def get_logger(name, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.hasHandlers():
        ch = logging.StreamHandler()
        ch.setLevel(level)
        formatter = logging.Formatter(
            fmt="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger


if __name__ == "__main__":
    logger = get_logger('test')
    logger.debug("DEBUG")

```





