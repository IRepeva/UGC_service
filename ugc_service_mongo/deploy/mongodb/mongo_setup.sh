#!/bin/bash

DB_NAME=movies
LIKES=likes
REVIEWS=reviews
BOOKMARKS=bookmarks
REVIEW_LIKES=review_likes

echo "~~~ Mongo initialization started ~~~"
echo "*** 1. Configuration server ***"
docker exec -it mongo-config-01 bash -c 'echo "rs.initiate({_id: \"rs-config-server\", configsvr: true, version: 1, members:[{_id:0, host: \"mongo-config-01:27017\"}, {_id: 1, host:\"mongo-config-02:27017\" }, {_id: 2, host:\"mongo-config-03:27017\"}]})" | mongosh'
echo "\n"

echo "*** 2. Assembly of replicas set ***"
docker exec -it shard-01-node-a bash -c 'echo "rs.initiate({_id: \"rs-shard-01\", version: 1, members: [{_id: 0, host : \"shard01-a:27017\" }, { _id: 1, host : \"shard01-b:27017\" }, { _id: 2, host : \"shard01-c:27017\" },]})" | mongosh'
sleep 5

docker exec -it shard-02-node-a bash -c 'echo "rs.initiate({ _id: \"rs-shard-02\", version: 1,members: [{ _id: 0, host : \"shard02-a:27017\" },{ _id: 1, host : \"shard02-b:27017\" }, { _id: 2, host : \"shard02-c:27017\" },]})" | mongosh'
sleep 5
echo "\n"

echo "*** 3. Adding shards to router ***"
docker exec -it router-01 bash -c 'echo "sh.addShard(\"rs-shard-01/shard01-a:27017\")" | mongosh'
docker exec -it router-01 bash -c 'echo "sh.addShard(\"rs-shard-01/shard01-b:27017\")" | mongosh'
docker exec -it router-01 bash -c 'echo "sh.addShard(\"rs-shard-01/shard01-c:27017\")" | mongosh'
sleep 5

docker exec -it router-01 bash -c 'echo "sh.addShard(\"rs-shard-02/shard02-a:27017\")" | mongosh'
docker exec -it router-01 bash -c 'echo "sh.addShard(\"rs-shard-02/shard02-b:27017\")" | mongosh'
docker exec -it router-01 bash -c 'echo "sh.addShard(\"rs-shard-02/shard02-c:27017\")" | mongosh'
sleep 3
echo "\n"

echo "*** 4. Database creation ***"
docker exec -it shard-01-node-a bash -c "echo \"use ${DB_NAME}\" | mongosh"
sleep 3
echo "\n"

echo "*** 5. Enable sharding for database ***"
docker exec -it router-01 bash -c "echo 'sh.enableSharding(\"${DB_NAME}\")' | mongosh"
sleep 3
echo "\n"

echo "*** 6. Collections creation ***"
docker exec -it router-01 bash -c "echo 'db.createCollection(\"${DB_NAME}.${LIKES}\")' | mongosh"
docker exec -it router-01 bash -c "echo 'db.createCollection(\"${DB_NAME}.${REVIEWS}\")' | mongosh"
docker exec -it router-01 bash -c "echo 'db.createCollection(\"${DB_NAME}.${BOOKMARKS}\")' | mongosh"
docker exec -it router-01 bash -c "echo 'db.createCollection(\"${DB_NAME}.${REVIEW_LIKES}\")' | mongosh"
sleep 3
echo "\n"

echo "*** 7. Sharding collections ***"
docker exec -it router-01 bash -c "echo 'sh.shardCollection(\"${DB_NAME}.${LIKES}\", {\"movie_id\": \"hashed\"})' | mongosh"
docker exec -it router-01 bash -c "echo 'sh.shardCollection(\"${DB_NAME}.${REVIEWS}\", {\"movie_id\": \"hashed\"})' | mongosh"
docker exec -it router-01 bash -c "echo 'sh.shardCollection(\"${DB_NAME}.${BOOKMARKS}\", {\"user_id\": \"hashed\"})' | mongosh"
docker exec -it router-01 bash -c "echo 'sh.shardCollection(\"${DB_NAME}.${REVIEW_LIKES}\", {\"review_id\": \"hashed\"})' | mongosh"
echo "\n"
echo "~~~ Mongo initialization finished ~~~"
