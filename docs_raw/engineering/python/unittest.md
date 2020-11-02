---
title: unittestにかかった時間を計測する
date: 2020-09-01
---



各テストの前には`setUp()`が実行され、テストの後に`tearDown()`が実行される。なのでその前後で`time()`を呼んで、その差分を表示させる。

```python
from time import time
import unittest

class TestStringMethods(unittest.TestCase):
    
    def setUp(self):
        self.time_begin = time()

    def tearDown(self):
        t = time() - self.time_begin
        print(f"{self.id()}: {t:.3f}s")
        
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')


if __name__ == '__main__':
    unittest.main()
```

実行するとこんな感じになる。

```sh
 $  python unittest_time.py
__main__.TestStringMethods.test_upper: 0.000s
.
----------------------------------------------------------------------
Ran 1 test in 0.001s

OK
```