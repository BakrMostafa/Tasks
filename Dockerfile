# syntax=docker/dockerfile:1
FROM python:3.12
ENV python3UNBUFFERED=1
COPY . /app/
WORKDIR /app
RUN apt-get upgrade
RUN apt-get update
RUN apt-get install -y cron
RUN apt-get install -y gunicorn
RUN pip install -U pip
RUN python3 -m pip install -r requirements.txt
RUN touch /var/log/cron.log
CMD /etc/init.d/cron start -f /var/log/cron.log &&\
    python3 manage.py makemigrations &&\
    python3 manage.py migrate --no-input &&\
    python3 manage.py collectstatic --no-input &&\
    python3 manage.py createcachetable &&\
    gunicorn --bind=0.0.0.0:8000 --workers=3 --timeout=5 --threads=10 project.wsgi:application
