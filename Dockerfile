# Start with the base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app/

# Copy the requirements file and install dependencies
COPY requirements.txt .

# Install necessary system dependencies, including dos2unix
RUN apt-get update && \
    apt-get install -y gcc default-libmysqlclient-dev dos2unix && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Convert line endings for start_django.sh to Unix format
RUN dos2unix start_django.sh

# Expose the application port
EXPOSE 8000

# Run the startup script
CMD ["./start_django.sh"]
