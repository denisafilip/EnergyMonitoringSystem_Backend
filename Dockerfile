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
ENV POSTGRES_HOST=postgres-integration
ENV POSTGRES_PORT=5432

RUN pip install --upgrade pip  

COPY ./DS2022_30441_Filip_Denisa_1_Backend $DockerHOME
RUN pip install -r requirements.txt
EXPOSE 8000

