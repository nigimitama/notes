FROM python:3.10
ENV WORKDIR=/workdir
WORKDIR $WORKDIR

RUN apt update && \
    apt install -y \
    graphviz\
    libopencv-dev

COPY requirements.txt .
RUN pip3 install -r requirements.txt

ENV JUPYTER_CONFIG_DIR=${WORKDIR}/.jupyter
ENV JUPYTERLAB_WORKSPACES_DIR=${WORKDIR}/.jupyter
