FROM python:3.9.12-slim-buster as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc

COPY ./requirements.txt requirements.txt

RUN pip install --user -r requirements.txt

FROM python:3.9.12-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /bot

ENV PATH=/root/.local/bin:$PATH
COPY --from=builder /root/.local /root/.local

COPY . .

CMD gunicorn main:main --bind 0.0.0.0:8081 --worker-class aiohttp.GunicornWebWorker