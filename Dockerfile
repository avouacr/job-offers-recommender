FROM python:3.8-slim

RUN adduser --disabled-login app_user

WORKDIR /home/app_user

RUN python -m venv venv
RUN apt-get update && apt-get install -y \
    build-essential \
    locales locales-all \
    texlive texlive-fonts-extra \
    ncdu \
 && rm -rf /var/lib/apt/lists/*
COPY requirements.txt requirements.txt
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY . .

RUN chmod +x boot.sh

ENV FLASK_APP app.py

RUN chown -R app_user:app_user ./
USER app_user

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
