import json
import boto3
import urllib.parse
import pandas as pd

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    try:
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
        bucket = event['Records'][0]['s3']['bucket']['name']
        if key.startswith('pace-data'):
            destination_bucket_name = 'data-raw-input'
            copy_source_object = {'Bucket': bucket, 'Key': key}
            s3.copy_object(CopySource=copy_source_object, Bucket=destination_bucket_name, Key='pace-data.csv')
    except Exception as e:
        return {
            'statusCode': 200,
            'body': json.dumps(e)
        }

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from S3 first events Lambda!')
    }

