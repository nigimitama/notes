#!/bin/bash
set -e

function build_book() {
    input=$1
    output=${1//md/html}
    echo $output
    pandoc $input \
        --output=$output.html \
        --standalone \
        --mathjax \
        --highlight-style tango \
        --css=modules/style.css \
        --template=template.html \
        --title-prefix=盆暗の勉強メモ \
        --toc
}


# reset
rm -r ./docs/*

# css, jsのフォルダを移動する
cp -r ./pandoc/modules ./docs/modules

# generate documents
cd docs_raw
files=$(find | grep .md)
echo "files: $files"
cd ..
for file in files; do
    echo $file
    build_book $file
done




