FROM ghcr.io/josxa/python-poetry-base:latest as Build

WORKDIR /letmebot

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-dev

COPY . ./
ENV SHELL=/bin/bash

CMD ["poetry", "run", "python", "-m", "letmebot.main"]
