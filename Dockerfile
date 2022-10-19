FROM python:3.9-buster

WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN apt update
RUN apt install ffmpeg -y

COPY src/ .

ENV interval=3600

ENTRYPOINT [ "python", "-u", "grabber.py" ]

LABEL MAINTAINER="Rutger Nijhuis"