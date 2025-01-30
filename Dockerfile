# Use the official Python image from the Docker Hub
FROM python:3.11-slim

RUN mkdir /log
RUN touch /log/error.log

WORKDIR /app

COPY requirements.txt /app
COPY docker/entrypoint.sh /app

RUN chmod +x entrypoint.sh

RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

COPY . /app

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
