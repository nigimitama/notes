

# 勉強の備忘録サイト



- 数式入りのmarkdownをhtmlにしたい
  - pandocを使いこなすことができれば、いけそう
- 静的サイトだけどlayoutを共通化して、変更の都度mdからhtmlにコンバートしたい
  - contentsはシンプルにmdを変換したhtmlで、それ以外はもっと凝った感じで
  - R markdownから変換したときのような目次をつけたい
  - `deploy.sh`を実行したら変換からpushまで全部される、みたいな



### 方法

- pandocでmarkdownをhtmlに変換する
- テンプレートのhtmlを作り、そのコンテンツ部分にmarkdownの内容を埋め込む形でjinja2で各記事のhtmlを吐き出す
  - h1, h2タグなどの見出しに対して自動で目次を振るようなスクリプトを書き、jinja2で吐き出すときに目次を追加できるようにする
- pandocのテンプレートというのもある
  - サイトのindex.htmlとそのテンプレートの共通化が大変そうなので使わないことにする。テンプレート関連は全部jinja2でやる


```
pandoc sample.md \
  --from=markdown \
  --output=sample.html \
  --standalone \
  --mathjax \
  --highlight-style tango \
  --toc \
  --css=github-pandoc.css
```



```
pandoc sample.md \
  --from=markdown \
  --output=output.html \
  --standalone \
  --mathjax \
  --highlight-style tango \
  --toc \
  --template=templates/default.html
```


```
pandoc sample.md \
  --output=sample.html \
  --standalone \
  --mathjax \
  --highlight-style tango \
  --template=templates/layout.html \
  --toc
```


### pandoc links

- [Pandoc User’s Guide 日本語版 — 日本Pandocユーザ会 2019.02.21 ドキュメント](https://pandoc-doc-ja.readthedocs.io/ja/latest/users-guide.html#using-pandoc)
- [Pandoc - Demos](https://pandoc.org/demos.html)
- [Pandoc で github 風 CSS を使った standalone な html を生成 - Qiita](https://qiita.com/griffin_stewie/items/95026360fdfca1bd8e33)
- [Pandocをインストールしてマークダウン記法を自分好みに変換しよう！ - はるなぴログ](https://www.halu7.com/entry/pandoc-install-option)
- [44種類のフォーマットに対応したPandocでMarkdownをHTML形式に変換する | Developers.IO](https://dev.classmethod.jp/articles/pandoc-markdown2html/)



### FrontEnd

#### Sticky Table of Contents
- toc generator: [Tocbot](https://tscanlin.github.io/tocbot/)
- [Sticky Table of Contents with Scrolling Active States | CSS-Tricks](https://css-tricks.com/sticky-table-of-contents-with-scrolling-active-states/)
- [Progress Nav](https://lab.hakim.se/progress-nav/)

