

# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.7.2

RUN pip install --upgrade pip

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

EXPOSE 8080

# Copy local code to the container image.
ENV APP_HOME /gcp-release-notes-app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install -r requirements.txt

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD streamlit run --server.port 8080 --server.enableCORS false app.py