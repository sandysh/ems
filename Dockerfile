# Dockerfile

# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Expose port 8000 to the outside world
EXPOSE 8000

# Run the Django development server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "employee_rating.wsgi:application"]

RUN apt -y update
RUN apt install -y curl
RUN curl -sL https://deb.nodesource.com/setup_20.x -o nodesource_setup.sh
RUN apt install -y nodejs
RUN apt install -y npm
