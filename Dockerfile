FROM python:3.9

# NOTE: Github ActionsではGITHUB_WORKSPACEに上書きされる
WORKDIR /workdir

RUN apt update && \
    apt install -y graphviz

COPY requirements.txt .
RUN pip3 install -r requirements.txt

ENV PROJECT_NAME="book/"
CMD ["jupyter-book", "build", "$PROJECT_NAME"]
