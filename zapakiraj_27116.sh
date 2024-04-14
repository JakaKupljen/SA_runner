#!/bin/bash

# Pass secrets as arguments or environment variables
DOCKER_USERNAME=$1
DOCKER_PASSWORD=$2
REPO_NAME=$3

# Log in to Docker using Docker login with a token
echo $DOCKER_PASSWORD | docker login --username $DOCKER_USERNAME --password-stdin

# Construct the tag using the current date and time
TAG="$(date +'%Y-%m-%d--%H-%M')"

# Build Docker image with the constructed tag
docker build . --file Dockerfile --tag $DOCKER_USERNAME/$REPO_NAME:$TAG

# Push Docker image to DockerHub
docker push $DOCKER_USERNAME/$REPO_NAME:$TAG
