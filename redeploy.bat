echo "Stopping and removing the back-end container"

docker stop  django-integration

docker rm  django-integration

echo "Removing the image for the back-end container"
docker image rm assignment1-django-integration

echo "Removing the volume for the back-end container"
docker volume rm  assignment1_django-integration


echo "Stopping and removing the front-end container"

docker stop angular-integration

docker rm angular-integration

echo "Removing the image for the front-end container"
docker image rm assignment1-angular-integration

echo "Stopping and removing the PostgreSQL container"

docker stop  postgres-integration

docker rm  postgres-integration

echo "Removing the image for the back-end container"
docker image rm postgres

echo "Removing the volume for the back-end container"
docker volume rm  assignment1_postgres-integration


docker-compose up --build