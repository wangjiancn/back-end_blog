FROM python:3.7.4-alpine

LABEL description="python with mysqlclient,pipenv,uwsgi, nginx, and r"
LABEL size="153mb"

# 在项目目录创建 .venv存放虚拟环境

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories && \
    apk add --no-cache mariadb-connector-c-dev &&\
    apk add --no-cache --virtual .build-deps build-base  mariadb-dev && \
    pip install --trusted-host=pypi.douban.com -i http://pypi.douban.com/simple/ --no-cache-dir pipenv 

WORKDIR /app

COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --system && apk del .build-deps
COPY blog .



EXPOSE 8000
EXPOSE 80

ENTRYPOINT gunicorn blog.wsgi -b 0.0.0.0:8000

