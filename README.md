# AuctionService

# Table of content
1. [About](#about)
2. [Installation](#installation)
    1. [GeneralGeneral Requirements](#1-general-requirements)
    2. [Running](#2-running)

# About
Auction Services, with using DRF and celery (redis broker
)
# Installation
#### 1. General Requirements
- PostgreSQL 9.xx < 10
- Docker
- Docker-compose
- Make sure to provide settings at `AuctionService/settings.py`

#### 2. Running
- Run `docker-compose build`
- Run `docker-compose run postgres`
- At another terminal run `docker exec -it postgres psql -U postgres ` and create database
- Run `docker-compose run django python manage.py makemigrtions` 
  and `docker-compose run django python manage.py migrate`
- Then use `docker-compose up`. If it returns error like `connection refused`
  run every docker image in different terminal: `docker-compose run {SERVICE}` (postgres, django, celery, redis)
