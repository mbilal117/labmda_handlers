#!/bin/bash
aws s3 mb s3://first-task-bucket
aws s3 mb s3://data-raw-input
aws s3 cp ./pace-data.csv s3://first-task-bucket/ --acl public-read
