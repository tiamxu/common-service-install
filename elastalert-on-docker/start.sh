#!/bin/bash
docker rm -f elastalert
docker run -itd --name elastalert \
 -v `pwd`/data:/opt/elastalert/data \
 -v `pwd`/elastalert.yaml:/opt/elastalert/config.yaml \
 -v `pwd`/rules:/opt/elastalert/rules \
 -v `pwd`/elastalert_modules:/opt/elastalert/elastalert_modules  \
 -e ELASTICSEARCH_HOST="10.11.3.219" \
 -e ELASTICSEARCH_PORT=9200 \
 -e CONTAINER_TIMEZONE="Asia/Shanghai"  \
 -e TZ="Asia/Shanghai" \
 -e SET_CONTAINER_TIMEZONE=True \
 -e ELASTALERT_BUFFER_TIME=10  \
 -e ELASTALERT_RUN_EVERY=1  \
 -e ELASTICSEARCH_USER="elastic" \
 -e ELASTICSEARCH_PASSWORD='admin@123,' \
 --add-host es-dev.xxx.net:192.168.1.1 \
 anjia0532/elastalert-docker:v0.2.4
