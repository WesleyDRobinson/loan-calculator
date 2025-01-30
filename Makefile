# Makefile for Docker

# Variables
IMAGE_NAME = loans
CONTAINER_NAME = django_loans
DOCKERFILE_PATH = .
PORT = 8000

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) $(DOCKERFILE_PATH)

# Run the Docker container
run:
	docker run -d --env-file ./.env.list -p $(PORT):8000 --name $(CONTAINER_NAME) $(IMAGE_NAME)

# Stop the Docker container
stop:
	docker stop $(CONTAINER_NAME)

# Remove the Docker container
rm:
	docker rm $(CONTAINER_NAME)

# Rebuild the Docker image and run the container
rebuild: stop rm build run

# Show logs from the Docker container
logs:
	docker logs -f $(CONTAINER_NAME)

# Clean up Docker images and containers
clean:
	docker system prune -f

.PHONY: build run stop rm rebuild logs clean