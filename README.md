# Image API

A basic image manipulation API made with Flask and Docker.

Base setup inspired by examples from Docker image tiangolo/uwsgi-nginx-flask:python3.8

## Setup (Docker)

1. Clone the repository

```
git clone git@github.com:martinbaste/simple-image-api.git
cd simple-image-api
```

2. Build and run the image

```
bash docker_start.sh
```

Server is accessible at http://localhost:8080/

## Setup (virtual environment)

1. Clone the repository

```
git clone git@github.com:martinbaste/simple-image-api.git
cd simple-image-api
```

2. Create virtual environment

```
python3 -m venv venv
```

3. Activate virtual environment and install dependencies

```
source venv/bin/activate
pip install -r requirements.txt
```

4. Run the server

```
bash dev_start.sh
```

## To improve

* Base image should be an official python base image
* Switch from venv to poetry
* Make sure no vulnerabilities are exposed when downloading images from URLs