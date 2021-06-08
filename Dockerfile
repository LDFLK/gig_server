FROM python:3.8-slim-buster
WORKDIR /gig_server

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY gig_server.py gig_server.py
COPY test_key.pem test_key.pem
COPY test_cert.pem test_cert.pem

EXPOSE 4001
CMD [ "gunicorn", "--workers", "16", "--certfile", "test_cert.pem", "--keyfile", "test_key.pem", "--bind", "0.0.0.0:4001", "gig_server:app"]
