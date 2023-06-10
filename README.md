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

1. update pip and install poetry in your server using pip

```bash
python -m pip install --upgrade pip
pip install poetry
```

2. build docker image for hotspots-api

```bash
bash hotspots-api/build.sh 
```

3. build docker image for fire visualizer web app
```bash
bash visualizer/build.sh 
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


>NOTE: this repository is still under development