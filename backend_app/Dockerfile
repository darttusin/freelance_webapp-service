FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /backend_app

COPY ./requirements.txt /backend_app/requirements.txt

RUN pip install -r requirements.txt 

COPY . /backend_app/ 

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
