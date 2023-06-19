FROM python:3.9
WORKDIR /workdir
RUN apt update && \
    apt install -y graphviz
COPY requirements.txt .
COPY requirements_no_deps.txt .
RUN pip3 install -r requirements.txt
RUN pip3 install -r requirements_no_deps.txt --no-deps
