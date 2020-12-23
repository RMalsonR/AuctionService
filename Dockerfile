FROM python:3.6
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/core
COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN pip install djangorestframework-simplejwt
COPY . /usr/src/core/