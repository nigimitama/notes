

# 勉強の備忘録サイト



- 数式入りのmarkdownをhtmlにしたい
  - pandocを使いこなすことができれば、いけそう
- 静的サイトだけどlayoutを共通化して、変更の都度mdからhtmlにコンバートしたい
  - contentsはシンプルにmdを変換したhtmlで、それ以外はもっと凝った感じで
  - R markdownから変換したときのような目次をつけたい
  - `deploy.sh`を実行したら変換からpushまで全部される、みたいな


### 案：トピックごと、長めの文書ごとにGitbookにする
- 目次機能→Gitbook(HonKit)で実現する
- トップページに各Gitbookへのリンクを置く



# 構成

## サーバー

- github pages



## レンダリング

- 方法１：すべての記事でheader、footerを入れる
  - jinja2でテンプレートする
    - layout.htmlにテンプレートを入れる
    - テンプレートから各記事を吐き出す

- ~~方法２：iframeをjsで書き換える~~
  - テンプレートのmain content部分を各記事のものに置き換える
  - こっちはマイナーな方法かも
  - あと見栄えが良くないかも



### 方法

- pandocでmarkdownをhtmlに変換する
- テンプレートのhtmlを作り、そのコンテンツ部分にmarkdownの内容を埋め込む形でjinja2で各記事のhtmlを吐き出す
  - h1, h2タグなどの見出しに対して自動で目次を振るようなスクリプトを書き、jinja2で吐き出すときに目次を追加できるようにする
- pandocのテンプレートというのもある
  - サイトのindex.htmlとそのテンプレートの共通化が大変そうなので使わないことにする。テンプレート関連は全部jinja2でやる


```
pandoc docs_raw/sample.md \
  --from=markdown \
  --output=output.html \
  --standalone \
  --mathjax \
  --highlight-style tango
```

### pandoc links
- [Pandoc User’s Guide 日本語版 — 日本Pandocユーザ会 2019.02.21 ドキュメント](https://pandoc-doc-ja.readthedocs.io/ja/latest/users-guide.html#using-pandoc)
- [Pandoc - Demos](https://pandoc.org/demos.html)
- [Pandoc で github 風 CSS を使った standalone な html を生成 - Qiita](https://qiita.com/griffin_stewie/items/95026360fdfca1bd8e33)
- 


