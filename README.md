# Fire Visualizer
A web app and REST API for forest fire visualizations


# Requirements

- Server with python3.11, docker compose, or docker (new version with compose included)
- Clone the repository and change directory
```bash
$ git clone https://github.com/yahuarlocro/fire-visualizer.git

$ cd fire-visualizer 
```

# Usage

First of all clone the reposi

1. create a virutal environment, update pip and install poetry in your server using pip

```bash
$ virtualenv -p python3.11 venv
$ source venv/bin/activate
$ python -m pip install --upgrade pip
$ pip install poetry
```

2. build docker image for hotspots-api

```bash
$ cd hotspots-api
$ bash build.sh 
```

3. build docker image for fire visualizer web app
```bash
$ cd ../visualizer
$ bash build.sh 
```

4. once the images are available locally, you can deploy the full application stack. If needed, do adapt the ***.env*** file.  The variables to be adapted are:
	- POSTGRES_HOST=172.17.0.1
	- REDIS_HOST=172.17.0.1
	- API_URL_BASE=http:\//172.17.0.1:8000
	
	The IP correspond to the docker0 network interface (gateway)

```bash
POSTGRES_USER=postgres
POSTGRES_PW=postgres
POSTGRES_HOST=172.17.0.1
POSTGRES_PORT=5433
POSTGRES_DB=hotspots
REDIS_HOST=172.17.0.1
REDIS_PORT=6379
API_URL_BASE=http://172.17.0.1:8000
SECRET_KEY=my-secret-key
VISUALIZER_PORT=5000
API_PORT=8000
IMAGE_TAG=0.1.0
```


5. deploy the containers
```bash
docker compose up -d
```


6. To access the web app go to http://localhost:5000
7. To access the REST API go to http://localhost:8000/docs

8. Upload data (***input-data.csv***) using the endpoint POST /hotspots/batch-upload. For more information you can check the openapi definitions in (once all services are running) http://localhost:8000/docs#/default/create_batch_hotspots_hotspots_batch_upload__post

>NOTE: this repository is still under development