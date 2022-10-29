FROM python:3.10.8
ENV DockerHOME=/home/app/webapp

RUN mkdir -p $DockerHOME  

WORKDIR $DockerHOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV TZ=UTC
ENV POSTGRES_DB=energy_platform
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=root
ENV POSTGRES_HOST=postgres_db
ENV POSTGRES_PORT=5432

RUN pip install --upgrade pip  

COPY . $DockerHOME  
RUN pip install -r requirements.txt  
EXPOSE 8000
CMD python manage.py migrate --noinput
CMD python manage.py runserver
