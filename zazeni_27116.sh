#!/bin/bash

# Pass secrets and tag as arguments or environment variables
DOCKER_USERNAME=$1
DOCKER_PASSWORD=$2
REPO_NAME=$3
TAG=$4

# Pull Docker image from DockerHub using the provided tag
docker pull $DOCKER_USERNAME/$REPO_NAME:$TAG

# Run Docker container
docker run -d -p 8080:80 $DOCKER_USERNAME/$REPO_NAME:$TAG
