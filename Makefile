docker_kafka = docker-compose exec kafka
docker_kafka_name = kafka
docker_kafka_port = 9093


run_and_config_db_research:
	docker-compose -f db_research/docker-compose.yml up -d --build && \
	chmod +x ./db_research/deploy/mongo_setup.sh && \
	sh ./db_research/deploy/mongo_setup.sh

run_and_config_ugc_mongo:
	docker-compose -f ugc_service_mongo/docker-compose.yml up -d --build && \
	chmod +x ./ugc_service_mongo/deploy/mongodb/mongo_setup.sh && \
	sh ./ugc_service_mongo/deploy/mongodb/mongo_setup.sh

run_ugc_mongo:
	@docker-compose -f ugc_service_mongo/docker-compose.yml up -d --build

config_mongo:
	chmod +x ./ugc_service_mongo/deploy/mongodb/mongo_setup.sh && \
	sh ./ugc_service_mongo/deploy/mongodb/mongo_setup.sh


fill_mongo_test_data:
	cd ugc_service_mongo && \
	docker-compose exec -it ugc_mongo python src/utils/fill_db.py && \
	cd ..