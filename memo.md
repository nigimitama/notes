

# 勉強の備忘録サイト

いくつかの方法を検討中

1. pandocでmd->htmlの変換をして、サイトは自分で作る
2. github pagesのjekyllの機能を使う
3. hoxoなどの外部のサービスを使う



## Github pages

- customize layout: [Adding a theme to your GitHub Pages site using Jekyll - GitHub Docs](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/adding-a-theme-to-your-github-pages-site-using-jekyll#customizing-your-themes-html-layout)
  - `_layout` ディレクトリをつくる
  - [Themes | Jekyll • Simple, blog-aware, static sites](https://jekyllrb.com/docs/themes/#overriding-theme-defaults)



## Jekyllを使う

- [Front Matter | Jekyll • Simple, blog-aware, static sites](https://jekyllrb.com/docs/front-matter/)
- Theme: [テーマ選択画面で GitHub Pages サイトにテーマを追加する - GitHub Docs](https://docs.github.com/ja/github/working-with-github-pages/adding-a-theme-to-your-github-pages-site-with-the-theme-chooser)

- [Jekyll を使用して GitHub Pages サイトをローカルでテストする - GitHub Docs](https://docs.github.com/ja/github/working-with-github-pages/testing-your-github-pages-site-locally-with-jekyll)





## pandocを使う場合

### 1. index.htmlなど
- jinja2でテンプレートから生成する
- data_science.htmlなどのカテゴリトップ画面も同様
- htmls/render_html.pyを実行

### 2. 個別の記事
- pandocのテンプレートを使う




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





