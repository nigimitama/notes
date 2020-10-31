pandoc sample.md \
  --output=sample.html \
  --standalone \
  --mathjax \
  --highlight-style tango \
  --css=style.css \
  --template=templates/layout.html \
  --title-prefix=盆暗の勉強メモ \
  --toc