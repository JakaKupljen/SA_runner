#!/bin/bash



docker pull $DOCKER_USERNAME/$REPO_NAME:$TAG

docker run -d -p 8080:80 $DOCKER_USERNAME/$REPO_NAME:$TAG
