FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /django
COPY requirements.txt /django/
RUN pip install -r requirements.txt
COPY . /django

# CMD gunicorn root.wsgi:application --bind 0.0.0.0:$PORT/