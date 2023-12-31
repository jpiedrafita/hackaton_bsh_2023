FROM ubuntu:latest

# Install additional dependencies, if needed
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip 

RUN pip install pandas \
    pip install plotly \
    pip install entsoe-py \
    pip install flask \
    pip install google-cloud-firestore

# WORKDIR /app
# # Copy the necessary files to the container
# COPY . /app

COPY . .

# Run any required commands
ENV FLASK_ENV=development
ENV FLASK_APP=app.py

EXPOSE 3000

CMD flask run --host=0.0.0.0 --port=3000
