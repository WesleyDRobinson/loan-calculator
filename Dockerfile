# Use the official Python image from the Docker Hub
FROM python:3.11-slim

WORKDIR /app

RUN mkdir -p /app/logs
RUN touch /app/logs/error.log

COPY requirements.txt /app
COPY docker/entrypoint.sh /app
COPY ./.env.list /app

RUN chmod +x /app/entrypoint.sh

RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

COPY . /app

# Expose the port the app runs on
EXPOSE 8000

# Set the entry point to the entrypoint.sh script
ENTRYPOINT ["/app/entrypoint.sh"]
