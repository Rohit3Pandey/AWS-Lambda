import boto3
import uuid
import os
import json
import time
from botocore.exceptions import ClientError

s3_client = boto3.client('s3')

def get_file_extension_from_key(key):
    # Replace spaces and parentheses with underscores
    key = key.replace(' ', '_').replace('(', '_').replace(')', '_')
    file_extension = os.path.splitext(key)[1][1:].lower()
    return file_extension

def create_destination_bucket_name(file_extension):
    return f"destination-bucket-{file_extension}"

def create_bucket_if_not_exists(bucket_name):
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} already exists.")
        return True
    except Exception as e:
        if e.response['Error']['Code'] == '404':
            s3_client.create_bucket(Bucket=bucket_name)
            print(f"Bucket {bucket_name} created successfully.")
            return True
        else:
            print(f"Error creating bucket {bucket_name}. Error: {str(e)}")
            return False

def move_object(source_bucket, object_key, destination_bucket):
    retry_attempts = 3  # Number of retry attempts
    retry_delay = 1  # Delay between retry attempts (in seconds)

    for attempt in range(1, retry_attempts + 1):
        try:
            # Check if the object exists in the source bucket
            s3_client.head_object(Bucket=source_bucket, Key=object_key)
            # Object exists, proceed with copy
            s3_client.copy_object(
                CopySource={'Bucket': source_bucket, 'Key': object_key},
                Bucket=destination_bucket,
                Key=object_key
            )
            # Delete the object from the source bucket
            s3_client.delete_object(Bucket=source_bucket, Key=object_key)
            print(f"Object {object_key} moved to {destination_bucket} successfully.")
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404' or e.response['Error']['Code'] == 'NoSuchKey':
                print(f"Object {object_key} not found in the source bucket.")
                if attempt < retry_attempts:
                    print(f"Retrying after {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print(f"All retry attempts exhausted. Moving object {object_key} failed.")
                    return False
            else:
                print(f"Error moving object {object_key} (Attempt {attempt}): {str(e)}")
                if attempt < retry_attempts:
                    print(f"Retrying after {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print(f"All retry attempts exhausted. Moving object {object_key} failed.")
                    return False
    return False

def lambda_handler(event, context):
    print("Received event:")
    print(json.dumps(event, indent=2))

    # Get the source bucket name from the event
    source_bucket = event['Records'][0]['s3']['bucket']['name']

    # Get the object key from the event
    object_key = event['Records'][0]['s3']['object']['key']

    # Get the file extension from the object key
    file_extension = get_file_extension_from_key(object_key)

    # Create the destination bucket name based on the file extension
    destination_bucket = create_destination_bucket_name(file_extension)

    # Check if the destination bucket exists
    create_bucket_if_not_exists(destination_bucket)

    # Move the object to the destination bucket
    move_object(source_bucket, object_key, destination_bucket)
