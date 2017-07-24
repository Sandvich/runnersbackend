FROM 3.5-alpine

COPY . /app

RUN pip install -r /app/requirements.txt && /app/seed.py

CMD /app/run.py
