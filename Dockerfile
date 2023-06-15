FROM ubuntu:latest
# Install additional dependencies, if needed
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip
RUN pip install -r req.txt
WORKDIR /app
# Copy the necessary files to the container
COPY . /app
# Run any required commands
RUN export FLASK_ENV=development \
    export FLASK_APP='app.py'
CMD flask run --host=0.0.0.0 --port=5000