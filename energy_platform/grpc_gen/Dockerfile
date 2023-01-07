FROM python:3.10.8
ENV DockerDIR=/home/app/grpc_gen

RUN mkdir -p $DockerDIR

WORKDIR $DockerDIR

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./DS2022_30441_Filip_Denisa_1_Backend/energy_platform/grpc_gen $DockerDIR
RUN pip install -r requirements.txt

# RUN python grpc_server.py