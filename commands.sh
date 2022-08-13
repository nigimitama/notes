#!bin/bash -eux

PROJECT_NAME="book/"

if [ ${1} = 'create' ]; then
    sudo docker-compose run workspace jupyter-book create $PROJECT_NAME
elif [ ${1} = 'build' ]; then
    sudo docker-compose run workspace jupyter-book build $PROJECT_NAME
elif [ ${1} = 'bash' ]; then
    sudo docker-compose run workspace bash
elif [ ${1} = 'jupyterlab' ]; then
    sudo docker-compose run --publish=8888:8888 workspace jupyter-lab --ip=0.0.0.0 --allow-root
else
    echo "Usage: bash ${0} [create|build|bash|jupyterlab]"
fi
