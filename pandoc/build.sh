pandoc sample.md \
  --output=sample.html \
  --standalone \
  --mathjax \
  --highlight-style tango \
  --template=templates/layout.html \
  --css=style.css \
  --toc