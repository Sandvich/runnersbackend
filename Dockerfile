FROM python:3.5-alpine

COPY . /app

RUN apk --update add musl-dev linux-headers g++ openssl libffi-dev \
	&& pip install -r /app/requirements.txt \
	&& rm /var/cache/apk/* \
	&& python /app/seed.py

CMD python /app/run.py
