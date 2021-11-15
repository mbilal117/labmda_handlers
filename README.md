# labmda_handlers
Steps to complete the task

* Sign Up AWS account
* Create New User (Administrator)
* Create Access Key ID and Secret
* Install AWS CLI (curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" unzip awscliv2.zip sudo ./aws/install)
* configure aws cli (aws configure)
* run the bash script (./script.sh) to create bucket and copy raw file into bucket
* give public read access permission to data-raw-input bucket
* create a lambda function (first_handler.py)
* Create a virtualenv, install pandas and psycopg2
* zip pacakges into folder and upload in lambda layer
* Create a postgres RDS and a table to store clean data
* create a lambda function (second_handler.py)
* Create inbound rule for 5432 to connect is from pgadmin client
