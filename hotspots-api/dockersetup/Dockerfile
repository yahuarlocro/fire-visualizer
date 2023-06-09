FROM python:3.11.0-slim-buster

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# expose port and define dis/*.whl variable to pass at build-time to the builder 
ARG WHL_FILENAME
EXPOSE 5000
EXPOSE 5432

# create appuser, set home working directory, chage ownership
RUN useradd -m appuser
WORKDIR /home/appuser/hotspots-api
# RUN mkdir /home/appuser/hotspots-api/logs
COPY main.py /home/appuser/hotspots-api/
RUN chown -R appuser:appuser /home/appuser/hotspots-api
USER appuser
ENV PATH=/home/appuser/.local/bin:$PATH

# upgrade pip
RUN python -m pip install --upgrade pip

# copy from local to container as appuser
# COPY --chown=appuser:appuser hotspots-api/ .
COPY --chown=appuser:appuser dist/ ./dist/

# install hotspots-api with python package
RUN python -m pip install ${WHL_FILENAME}

# remove distribution file
RUN rm -rf dist

# Web Server Gateway Interface for production deployment
# CMD ["uvicorn", "--bind", "0.0.0.0:5000", "main:app"]
CMD ["uvicorn", "main:app"]
