#!/bin/bash
set -e

function build_book_ {
    input_md_path=$1
    # basename=${input_md_path##*/}
    output_html_path=${input_md_path//\.\//}  # remove ./
    output_html_path=${output_html_path//\//_}  # replace / with _
    output_html_path=${output_html_path//.md/.html}  # replace .md with .html
    pandoc $input_md_path \
        --output=$output_html_path \
        --standalone \
        --self-contained \
        --mathjax \
        --highlight-style tango \
        --css="modules/style.css" \
        --template="modules/template.html" \
        --title-prefix=盆暗の勉強メモ \
        --toc
}


function build_book {
    input_md_path=$1
    wd=$(pwd)
    dirname=${input_md_path%/*}
    cd $dirname
    basename=${input_md_path##*/}
    output_html_path=${basename//.md/.html}  # replace .md with .html
    pandoc $basename \
        --output=$output_html_path \
        --standalone \
        --self-contained \
        --mathjax \
        --highlight-style tango \
        --css="$wd/modules/style.css" \
        --template="$wd/modules/template.html" \
        --title-prefix=盆暗の勉強メモ \
        --toc
}

# reset
rm -r ./docs/*

# css, jsのフォルダを移動する
cp -r ./pandoc/modules ./docs

# markdownファイルを移動する
cp -r ./docs_raw/* ./docs

# generate documents
cd ./docs
files=$(find | grep .md)
echo "files: $files"
for file in $files; do
    if [[ $file != *"README"* ]]; then
        build_book $file
    fi
done
rm $files



