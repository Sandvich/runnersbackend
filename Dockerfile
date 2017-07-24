FROM python:3.5-alpine

COPY . /app

RUN apk add --no-cache add musl-dev linux-headers g++

RUN pip install -r /app/requirements.txt && /app/seed.py

CMD /app/run.py
