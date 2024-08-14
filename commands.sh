#!bin/bash -eux

PROJECT_NAME="book/"

if [ ${1} = 'create' ]; then
    sudo docker-compose run notes jupyter-book create $PROJECT_NAME
elif [ ${1} = 'build' ]; then
    sudo docker-compose run notes jupyter-book build $PROJECT_NAME
elif [ ${1} = 'bash' ]; then
    sudo docker-compose run notes bash
elif [ ${1} = 'jupyterlab' ]; then
    # docker-compose up あるいは commands.sh jupyterlab でjupyter起動
    sudo docker-compose run --publish=8888:8888 notes jupyter-lab --ip=0.0.0.0 --allow-root
elif [ ${1} = 'push' ]; then
	git add .
	git commit -m "update"
	git push
else
    echo "Usage: bash ${0} [create|build|bash|jupyterlab]"
fi
