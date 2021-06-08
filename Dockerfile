FROM python:3.8-slim-buster
WORKDIR /gig_server

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY gig_server.py gig_server.py

EXPOSE 4001
CMD [ "gunicorn", "--bind", "0.0.0.0:4001", "gig_server:app"]
