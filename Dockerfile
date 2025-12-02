# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc
# PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose the port the app runs on
# We'll default to 5000, but this is just documentation
EXPOSE 5000

# Run the application using Gunicorn
# We use "app:create_app()" factory pattern
# Bind to 0.0.0.0:$PORT (defaulting to 5000 if PORT is not set)
CMD gunicorn -w 4 -b 0.0.0.0:${PORT:-5000} "app:create_app()"
