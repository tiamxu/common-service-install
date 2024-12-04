#!/bin/bash
docker cp docker-entrypoint.sh  elastalert:/opt/docker-entrypoint.sh
docker restart elastalert
