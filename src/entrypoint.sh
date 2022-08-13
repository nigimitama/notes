PROJECT_NAME="site"

if [ ! -e $PROJECT_NAME ]; then
    jekyll new $PROJECT_NAME
fi

cd $PROJECT_NAME

bundle add webrick
bundle install
bundle exec jekyll serve --host 0.0.0.0
