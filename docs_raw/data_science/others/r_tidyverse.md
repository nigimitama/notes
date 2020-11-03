---
title: '[R] tidyverseの基本的な使い方のメモ'
date: 2019-01-19
---



Rにはデータの処理を効率的に行うことができるtidyverseというパッケージ群がある。ggplot2とかdplyrとかが含まれる。

これらのパッケージの関数たちのうち、使用頻度が非常に高いものをメモする。



# tidyverseとは

R界の「神」と呼ばれることも多い[Hadley Wickham](http://hadley.nz/)が作ったパッケージ群で、Rでの諸々の処理をモダンに行うことを可能にしている。

- GitHub:https://github.com/tidyverse/tidyverse



### the core tidyverse packages

tidyverseには以下のようなパッケージが含まれる。

- [ggplot2](http://ggplot2.tidyverse.org/) ：データの可視化のためのパッケージ。綺麗なグラフやGIS（統計地図）などを描ける
- [dplyr](http://dplyr.tidyverse.org/)：データの操作のためのパッケージ
- [tidyr](http://tidyr.tidyverse.org/)：整然データ
- [readr](http://readr.tidyverse.org/)：データの読み込みを便利にする
- [purrr](http://purrr.tidyverse.org/)：関数型プログラミングのためのパッケージ。リストの操作を便利にします。
- [tibble](http://tibble.tidyverse.org/)：モダンなデータフレームのパッケージ
- [stringr](https://github.com/tidyverse/stringr)：文字列の操作のためのパッケージ
- [forcats](https://github.com/hadley/forcats)：factorの操作のためのパッケージ





# よく使う関数・演算子

## パイプ演算子「%>%」

{magrittr}の機能のひとつである**パイプ演算子は、関数同士をつなげることができる。**

`%>%`の左辺にあるオブジェクトを、`%>%`の右辺にある関数の第一引数に送る。

例えば、irisのデータフレームを使って

1. `Species`変数が`"virginica"`の値のものだけを取り出す（`base::subset()`）
2. そのうち上から6行を表示する（`base::head()`）

という処理をしたいときは、パイプでデータと２つの関数をつなぎ合わせて１行で書くことができる。

```{r}
iris %>% subset(Species == "virginica") %>% head()
```

```
##     Sepal.Length Sepal.Width Petal.Length Petal.Width   Species
## 101          6.3         3.3          6.0         2.5 virginica
## 102          5.8         2.7          5.1         1.9 virginica
## 103          7.1         3.0          5.9         2.1 virginica
## 104          6.3         2.9          5.6         1.8 virginica
## 105          6.5         3.0          5.8         2.2 virginica
## 106          7.6         3.0          6.6         2.1 virginica
```

「`%>%`なんて打ち辛すぎるだろ！」と思うかもしれないが、RStudioでは「Ctrl+Shift+M」でパイプ演算子を（両側の半角スペースも一緒に）打ち込んでくれるので、1秒もかからず打つことができる。

適度に改行・代入して区切りながらパイプでつなげていくことで、コードの可読性を飛躍的に高めることができる。




## read_csv：データを適切な型で読み込む

{readr}の`read_csv`は、**データ型をしっかり判断しながらcsvを読み込んでくれる関数**である。

例えば地方自治体コードのようにゼロからはじまる数字のあるコードを読み込むとき、
`read.csv`を使うとinteger（整数型）として読み込むため、`01100`が`1100`にされてしまう。これではコードとして意味を成さなくなってしまう。

一方、`read_csv`を使えばゼロから始まっていることを考慮してcharacter（文字列型）として読み込んでくれるため、きちんとデータを利用できる。

```r
# city code data from RESAS
## base::read.csv
cities_base = read.csv("data/cities.csv")
str(cities_base)
```

```
## 'data.frame':    1920 obs. of  3 variables:
##  $ prefCode: int  1 1 1 1 1 1 1 1 1 1 ...
##  $ cityCode: int  1100 1101 1102 1103 1104 1105 1106 1107 1108 1109 ...
##  $ cityName: Factor w/ 1887 levels "あきる野市","あさぎり町",..: 624 629 634 630 632 633 631 628 625 626 ...
```



```R
## readr::read_csv
cities_readr = read_csv("data/cities.csv", locale = locale(encoding = "cp932"))
str(cities_readr)
```

```
## Classes 'tbl_df', 'tbl' and 'data.frame':    1920 obs. of  3 variables:
##  $ prefCode: int  1 1 1 1 1 1 1 1 1 1 ...
##  $ cityCode: chr  "01100" "01101" "01102" "01103" ...
##  $ cityName: chr  "札幌市" "札幌市中央区" "札幌市北区" "札幌市東区" ...
##  - attr(*, "spec")=List of 2
##   ..$ cols   :List of 3
##   .. ..$ prefCode: list()
##   .. .. ..- attr(*, "class")= chr  "collector_integer" "collector"
##   .. ..$ cityCode: list()
##   .. .. ..- attr(*, "class")= chr  "collector_character" "collector"
##   .. ..$ cityName: list()
##   .. .. ..- attr(*, "class")= chr  "collector_character" "collector"
##   ..$ default: list()
##   .. ..- attr(*, "class")= chr  "collector_guess" "collector"
##   ..- attr(*, "class")= chr "col_spec"
```

ただ、`read_csv`を使うときはエンコーディングに注意する必要がある。（特にWindowsでは）

Shift-JISやCP932でエンコードされているcsvデータ（Excelで文字化けせず開ける日本語を含むcsvデータ）を`read_csv`で開くときは、そのまま開くと日本語が文字化けするので、引数に`locale = locale(encoding = "cp932")`を指定する必要がある。



## select：列を選択する

`select()`は**データフレームから任意の列を取り出す関数**である。

{dplyr}パッケージはどの関数もよく使うが、とりわけ`select()`はとてもよく使う。

#### 基本：`select(data, 取り出したい列名, ...)`

```{r}
iris %>% select(Petal.Length, Petal.Width, Species) %>% head()
```

```
##   Petal.Length Petal.Width Species
## 1          1.4         0.2  setosa
## 2          1.4         0.2  setosa
## 3          1.3         0.2  setosa
## 4          1.5         0.2  setosa
## 5          1.4         0.2  setosa
## 6          1.7         0.4  setosa
```



#### `select()`内で使える演算子

- `-`：取り出したくない列を指定する
- `:`：ある列からある列までを取り出す
- `c()`：列名のベクトルで指定する



#### `select(関数)`

`select()`内で使う関数もある。

- `starts_with()`, `ends_with()`, `contains()`
  - 特定の文字列から始まる/特定の文字列で終わる/特定の文字列を含む、ような列を指定する
  - `iris %>% select(contains("Length"))`のように使う
- `matches()`：正規表現にマッチする列を指定する
- `num_range()`：列名に番号が振られている場合、番号の範囲に基づいて列を指定できる
- `one_of()`：列名の文字列ベクトルで列を指定できる
- `everything()`：全ての列を指定する。
  - 列の並び順を変えたいとき,`iris %>% select(Species, everything())`のように書く

`contains()`と`everything()`は個人的によく使う。




## rename：列名を変更する

`rename(data, [新列名] = [現列名], ...)`のように書く

```{r}
rename(iris, petal_length = Petal.Length) %>% head()
```

```
##   Sepal.Length Sepal.Width petal_length Petal.Width Species
## 1          5.1         3.5          1.4         0.2  setosa
## 2          4.9         3.0          1.4         0.2  setosa
## 3          4.7         3.2          1.3         0.2  setosa
## 4          4.6         3.1          1.5         0.2  setosa
## 5          5.0         3.6          1.4         0.2  setosa
## 6          5.4         3.9          1.7         0.4  setosa
```

なお、`select()`でも列名変更はできるが、返ってくるデータフレームには選択された列しか残らない。

#### `rename()`内で使える演算子、関数

`select()`と同じ。



## spread：ワイド形式（横持ち）にする

{tidyr}の`spread`と`gather`もよく使う関数の一つである。

`spread`はロング形式（縦持ち）のデータフレームをワイド形式（横持ち）にする。

`spread(data, key, value, fill = NA, ...)`

例えば以下のようなロング形式のデータフレームがあるときを考える。

```{r}
# 顧客id, 商品, 売上個数のデータ
sales <- data_frame(id = c(1:4, 1),
                    item = c("apple", "orange", "apple", "orange", "banana"),
                    count = c(3, 4, 1, 2, 3))
sales
```

```
## # A tibble: 5 x 3
##      id item   count
##   <dbl> <chr>  <dbl>
## 1     1 apple      3
## 2     2 orange     4
## 3     3 apple      1
## 4     4 orange     2
## 5     1 banana     3
```

`spred()`にid以外の列を入れ、keyにitem列、valueにcount列を指定する。

```{r}
sales %>% spread(key = item, value = count)
```

```
## # A tibble: 4 x 4
##      id apple banana orange
##   <dbl> <dbl>  <dbl>  <dbl>
## 1     1     3      3     NA
## 2     2    NA     NA      4
## 3     3     1     NA     NA
## 4     4    NA     NA      2
```

key（item列）の値ごとに新たな列が追加されていき、その中にはid列と対応したcount列の値が入った、ワイド形式の横長なデータフレームになった。




## gather：ロング形式（縦持ち）にする

`tidyr::gather()`はワイド形式のデータフレームをロング形式に変える

`gather(data, key = "key", value = "value", ..., na.rm = FALSE)`

- `key, value`：新しいkey列、value列の名前
- `na.rm`：NAの列を削除するかどうか

```{r}
sales %>% spread(item, count) %>% gather(item, count, apple:orange, na.rm = TRUE)
```

```
## # A tibble: 5 x 3
##      id item   count
## * <dbl> <chr>  <dbl>
## 1     1 apple      3
## 2     3 apple      1
## 3     1 banana     3
## 4     2 orange     4
## 5     4 orange     2
```

もとのロング形式に戻すことができた。