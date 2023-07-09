FROM python:3.10

RUN mkdir /app
RUN mkdir /app/staticfiles
RUN mkdir /app/mediafiles
ENV app=/app/web
WORKDIR /app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app

CMD ["python", "manage.py runserver"]