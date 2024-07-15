# BUILD:
# 		docker compose build

# BUILD-NC:
# 		docker-compose build --no-cache

# BUILD-PROGRESS:
# 		docker-compose build --progress --progress=plain

# DOWN:
# 		docker-compose down --volumes

# RUN:
# 		make DOWN && docker compose up

# RUN-SCALED:
# 		make DOWN && docker compose up --scale spark-worker=3

# RUN-D:
# 		make DOWN && docker compose up -d

# STOP:
# 		docker-compose stop

# SUBMIT:
# 		docker-compose exec da-spark-master spark-submit --master spark://spark-master:7077 --deploy-mode client ./apps/$(app)


build:
	docker-compose build

build-nc:
	docker-compose build --no-cache

build-progress:
	docker-compose build --no-cache --progress=plain

down:
	docker-compose down --volumes --remove-orphans

run:
	make down && docker-compose up

run-scaled:
	make down && docker-compose up --scale spark-worker=3

run-d:
	make down && docker-compose up -d

stop:
	docker-compose stop

submit:
	docker exec da-spark-master spark-submit --master spark://spark-master:7077 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 --deploy-mode client ./apps/$(app)

submit-da-book:
	make submit app=data_analysis_book/$(app)

rm-results:
	rm -r book_data/results/*