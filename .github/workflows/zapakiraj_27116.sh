#!/bin/bash

# Set environment variables
DOCKER_USERNAME=${{ secrets.DOCKER_USERNAME }}
DOCKER_PASSWORD=${{ secrets.DOCKER_PASSWORD }}
REPONAME=${{ secrets.REPO_NAME }}

# Log in to DockerHub
docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD

# Build Docker image
docker build . --file Dockerfile --tag $DOCKER_USERNAME/$REPONAME:latest

# Push Docker image to DockerHub
docker push $DOCKER_USERNAME/$REPONAME:latest
