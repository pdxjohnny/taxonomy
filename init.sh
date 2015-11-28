#!/bin/sh

MONGO='taxonomy-mongo'

docker stop ${MONGO}
docker rm ${MONGO}
docker run -d --name ${MONGO} -p 27017:27017 mongo
cat section | python import.py
