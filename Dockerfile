FROM python:3.12.6

RUN pip install --upgrade pip && \
    pip install poetry

WORKDIR /app

COPY . .

RUN poetry install

CMD ["poetry", "run", "fastapi", "dev", "app/main.py", "--host", "0.0.0.0"]