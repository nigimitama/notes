FROM python:3.10
WORKDIR /workdir

RUN apt update && \
    apt install -y \
    graphviz\
    libopencv-dev

COPY requirements.txt .
RUN pip3 install -r requirements.txt
