# Use the official Python 3.11 slim image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app/

# Copy the requirements file
COPY requirements.txt .

# Install dependencies and MySQL client libraries
RUN apt-get update
RUN apt-get install -y gcc default-libmysqlclient-dev -y
RUN pip install -r requirements.txt
RUN dos2unix start_django.sh
# Copy the project files into the container
COPY . .

# Expose the Django application port
EXPOSE 8000
# Run the Django development server
CMD ["sh","start_django.sh"]
