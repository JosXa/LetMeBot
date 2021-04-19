FROM arm32v7/python:3.8-slim AS PoetryBase

RUN apt-get update
RUN apt-get install -y git curl libpq-dev gcc

# https://github.com/python-poetry/poetry/issues/1579#issuecomment-598570212
RUN python -m venv "/opt/venv"
RUN . /opt/venv/bin/activate
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - -y
ENV PATH="/root/.poetry/bin:/opt/venv/bin:$PATH"
RUN poetry config virtualenvs.create false

RUN python -m pip install --upgrade pip

# Most of my projects use Poe as a script runner
RUN pip install poethepoet

ENV PYTHONUNBUFFERED=1

FROM PoetryBase AS Build

WORKDIR /letmebot

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-dev

COPY . ./
ENV SHELL=/bin/bash

CMD ["poetry", "run", "python", "-m", "letmebot.main"]
