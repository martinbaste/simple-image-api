#!/bin/bash

app="docker.test"

docker build -t ${app} .

# docker run -d -p 56733:80 \
#   --name=${app} ${app}# \
  #-v $PWD:/app ${app}

docker run -d -p 8080:80 ${app}

echo "Docker container should be running"

echo "Open http://localhost:8080"