from python:3.6.10-alpine3.11

ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.0.5 \
    POETRY_VIRTUALENVS_CREATE=false \
    APPENV=${ENV}

RUN apk update && apk add supervisor python3 python3-dev postgresql-dev libffi-dev libxml2-dev libxslt-dev openssl-dev postgresql-dev py3-setuptools freetype-dev jpeg-dev libwebp-dev tiff-dev libpng-dev lcms2-dev openjpeg-dev zlib-dev curl build-base py3-cryptography gcc make

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry install $(test $APPENV==production && echo "--no-dev") --no-interaction --no-ansi

COPY . /app
