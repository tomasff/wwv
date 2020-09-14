#!/bin/bash

docker build -t wwv_bot -f ./bot/Dockerfile .
docker build -t wwv_web -f ./web/Dockerfile .