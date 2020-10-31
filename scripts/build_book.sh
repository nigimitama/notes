#!/bin/bash

function build_book(file) {
    pandoc $file \
        --output=$file.html \
        --standalone \
        --mathjax \
        --highlight-style tango \
        --css=modules/style.css \
        --template=template.html \
        --title-prefix=盆暗の勉強メモ \
        --toc
}
