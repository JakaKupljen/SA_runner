#!/bin/bash


echo $DOCKER_PASSWORD | docker login --username $DOCKER_USERNAME --password-stdin

docker build . --file Dockerfile --tag $DOCKER_USERNAME/$REPO_NAME:$TAG

docker push $DOCKER_USERNAME/$REPO_NAME:$TAG
