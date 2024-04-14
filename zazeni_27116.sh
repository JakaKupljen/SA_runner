#!/bin/bash

# Pull Docker image from DockerHub
docker pull $DOCKER_USERNAME/$REPO_NAME:$TAG

# Run Docker container
docker run -d -p 8080:80 $DOCKER_USERNAME/$REPO_NAME:$TAG
