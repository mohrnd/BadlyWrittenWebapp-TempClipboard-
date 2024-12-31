#!/bin/bash -ex
yum install -y python3
yum install -y unzip
yum install -y python3-pip
sudo pip3 install flask mysql_connector_python boto3
mkdir Webapp
cd Webapp
wget <LinkToZip>
unzip <Name>.zip
export SECRET_KEY=<SecretKey>
export DATABASE_HOST=<DBhost>
export DATABASE_USER=<DBuser>
export DATABASE_PASSWORD=<DBPassword>
export DATABASE_DB_NAME=<DBName>
export DYNAMODB_NAME=<DynamoDBTableName>
export REGION=<Region>
FLASK_APP=app.py /usr/local/bin/flask run --host=0.0.0.0 --port=80
