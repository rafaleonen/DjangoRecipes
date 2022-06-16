FROM python:3

ENV PORT 8000

# Create app directory
RUN mkdir -p /usr/app
WORKDIR /usr/app

# Installing dependecies
COPY requirements.txt /usr/app
RUN pip install -r requirements.txt

# Copying source files
COPY . /usr/app

EXPOSE 8000