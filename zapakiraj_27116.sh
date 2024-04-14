#!/bin/bash

# Pass secrets and tag as arguments or environment variables
DOCKER_USERNAME=$1
DOCKER_PASSWORD=$2
REPO_NAME=$3
TAG=$4

# Log in to Docker using Docker login with a token
echo $DOCKER_PASSWORD | docker login --username $DOCKER_USERNAME --password-stdin

# Build Docker image with the provided tag
docker build . --file Dockerfile --tag $DOCKER_USERNAME/$REPO_NAME:$TAG

# Push Docker image to DockerHub
docker push $DOCKER_USERNAME/$REPO_NAME:$TAG
