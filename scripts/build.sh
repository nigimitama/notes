#!/bin/bash
set -e

echo "generate pandoc template -------------------"
cd ./htmls
python3 ./render_template.py
cd ..

echo "generate articles -------------------"

function build_page {
    input_md_path=$1
    # dirname=${input_md_path%/*}
    # cd $dirname
    output_html_path=${input_md_path//\.\//}  # remove ./
    output_html_path=${output_html_path//\//_}  # replace / with _
    output_html_path=${output_html_path//.md/.html}  # replace .md with .html
    pandoc $input_md_path \
        --output=$output_html_path \
        --standalone \
        --mathjax \
        --highlight-style tango \
        --css="modules/style.css" \
        --template="modules/pandoc_template.html" \
        --title-prefix=盆暗の勉強メモ \
        --toc
}


# reset
if [ -e ./docs ]; then
    rm -r ./docs
fi
mkdir ./docs

# css, jsのフォルダを移動する
cp -r ./pandoc/modules ./docs

# markdownファイルを移動する
cp -r ./docs_raw/* ./docs


# assetsフォルダをhtmlと同じ階層に移動する
cd ./docs
assets_dirs=$(find -type d | grep .assets)
# echo "assets_paths: $assets_paths"
for assets_dir in $assets_dirs; do
    mv "$assets_dir" .
done


# generate documents: htmlをすべて一番浅い階層に生成する
files=$(find | grep .md)
echo "files: $files"
for file in $files; do
    if [[ $file != *"README"* ]]; then
        build_page $file
    fi
done

# markdownファイルを削除
rm $files

# 空のディレクトリを削除
rm -r $(find . -type d -empty)

echo "generate index pages -------------------"
cd ../htmls
python3 ./render_html.py
