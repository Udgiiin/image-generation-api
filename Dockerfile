# pull official base image
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 8000
# add app
COPY . .