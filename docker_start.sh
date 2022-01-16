#!/bin/bash

app="docker.test"

docker build -t ${app} .

# docker run -d -p 56733:80 \
#   --name=${app} ${app}# \
  #-v $PWD:/app ${app}

docker run -d -p 56733:80 ${app}