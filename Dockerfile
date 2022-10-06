FROM python:3.10.4-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1 

WORKDIR /app
# informative
EXPOSE 8000  
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .