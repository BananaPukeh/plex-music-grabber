FROM python:3.8

WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY grabber.py .

ENV library_path="/library"
ENV interval=3600

VOLUME [ "/library" ]

ENTRYPOINT [ "python", "-u", "grabber.py" ]

LABEL MAINTAINER="Rutger Nijhuis"