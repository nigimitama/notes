FROM node:9-slim

WORKDIR /root/books

RUN apt update && \
    apt install -y vim

# gitbook
RUN npm install gitbook-cli -g

# honkit cause error
# RUN npm init --yes && \
#     npm install honkit --save-dev

CMD bash
