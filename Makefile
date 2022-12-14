docker_kafka = docker-compose exec kafka
docker_kafka_name = kafka
docker_kafka_port = 9093


run_and_config_db_research:
	docker-compose -f db_research/docker-compose.yml up -d --build && \
	chmod +x ./db_research/deploy/mongo_setup.sh && \
	sh ./db_research/deploy/mongo_setup.sh

run_db_research:
	docker-compose -f db_research/docker-compose.yml up -d --build

run_and_config_ugc:
	docker-compose -f ugc/docker-compose.yml up -d --build && \
	chmod +x ./ugc/deploy/mongodb/mongo_setup.sh && \
	sh ./ugc/deploy/mongodb/mongo_setup.sh

run_ugc:
	@docker-compose -f ugc/docker-compose.yml up -d --build

config_mongo:
	chmod +x ./ugc/deploy/mongodb/mongo_setup.sh && \
	sh ./ugc/deploy/mongodb/mongo_setup.sh


fill_mongo_test_data:
	cd ugc && \
	docker-compose exec -it ugc python src/utils/fill_db.py && \
	cd ..