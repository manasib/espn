FROM python:3.11-buster
RUN pip install poetry==2.1.1
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache
WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR
COPY . /app

EXPOSE 8080
USER docker


CMD ["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "8080" ,"--reload"]