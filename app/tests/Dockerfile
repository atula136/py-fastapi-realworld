# Use the official Python image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any necessary libraries in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install testing dependencies (e.g., pytest)
RUN pip install pytest pytest-cov

# Set environment variables for the app
ENV ENVIRONMENT=test

# Run pytest by default
CMD ["pytest", "--cov=app", "--cov-report=term", "app/tests"]

