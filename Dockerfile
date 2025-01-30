# Use the official Python image from the Docker Hub
FROM python:3.11-slim

RUN mkdir -p /log
RUN touch /log/error.log

WORKDIR /app

COPY requirements.txt /app/

RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

COPY . /app/

# Run migrations to set up the SQLite database
RUN python manage.py makemigrations
RUN python manage.py migrate

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
