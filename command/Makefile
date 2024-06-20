# General vars

docker_file = ../docker/docker-compose.yml
docker_compose = sudo docker-compose -f $(docker_file)

# Commands
HELP:
	echo "Try some of the followings commands:\n"\
	echo "make RUNSERVER: Run server"\
	echo "make CLOSESERVER: Close server"\
	echo "make BUILDSERVER: Build Docker Image"

RUNSERVER:
	$(docker_compose) up -d

CLOSESERVER:
	$(docker_compose) down

BUILDSERVER:
	$(docker_compose) build

LOGS:
	$(docker_compose) logs

CLEANVOLUMES:
	$(docker_compose) down -v

REBOOT:
	make CLOSESERVER
	make RUNSERVER
