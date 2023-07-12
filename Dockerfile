FROM python:3.10


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /mentor

COPY ./requirements.txt /mentor/

RUN pip install -r /mentor/requirements.txt

ADD . /mentor