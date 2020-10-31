pandoc sample.md \
  --output=sample.html \
  --standalone \
  --mathjax \
  --highlight-style tango \
  --css=templates/style.css \
  --template=templates/layout.html \
  --toc