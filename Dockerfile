FROM python:3.12-slim

# Install netcat-openbsd
RUN apt-get update && \
    apt-get install -y netcat-openbsd

# Set the working directory
WORKDIR /app

# Copy application code
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the wait-for-it script into the container
COPY wait-for-it.sh /usr/local/bin/wait-for-it
RUN chmod +x /usr/local/bin/wait-for-it

# Run Alembic migrations and then start the Uvicorn server
# ENTRYPOINT ["wait-for-it", "db_dev", "3306", "--", "sh", "-c", "alembic upgrade head && uvicorn app.main:app --reload --env-file .env.dev --host 0.0.0.0 --port 8000"]

ENTRYPOINT ["sh", "-c", "wait-for-it db_dev 3306 -- alembic upgrade head && uvicorn app.main:app --reload --env-file .env.dev --host 0.0.0.0 --port 8000"]


# Expose the port Uvicorn will run on
EXPOSE 8000
