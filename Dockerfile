FROM python:3.11-slim
WORKDIR /app/
COPY requirements.txt .
RUN apt-get update
RUN apt-get install gcc default-libmysqlclient-dev -y
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "MovieDB/manage.py", "runserver","0.0.0.0:8000"] 

