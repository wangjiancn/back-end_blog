FROM python:3.7.4-alpine@sha256:6673d8ce9610d166b6d7d6abda21537ddcf30e6bc8c20ca86f17f1085e20ac95

LABEL org.opencontainers.image.source="https://github.com/wangjiancn/back-end_blog"

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
    && apk add --no-cache mariadb-connector-c-dev \
    && apk add --no-cache --virtual .build-deps build-base mariadb-dev \
    && pip install --no-cache-dir --index-url https://pypi.tuna.tsinghua.edu.cn/simple pipenv==2022.12.19

WORKDIR /app

COPY Pipfile Pipfile.lock ./
RUN PIPENV_PYPI_MIRROR=https://pypi.tuna.tsinghua.edu.cn/simple pipenv sync --system \
    && apk del .build-deps

COPY blog ./
RUN sed -i 's/^from settings import /from blog.settings import /' utils/qiniu_tool.py

ARG version=unknown
LABEL com.my-ops.source-revision=$version

EXPOSE 8000

ENTRYPOINT ["gunicorn", "blog.wsgi", "-b", "0.0.0.0:8000"]
