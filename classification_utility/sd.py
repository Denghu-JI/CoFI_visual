import boto3
import json

# Set up the S3 client
s3 = boto3.client('s3')

# Load the existing JSON file from S3
bucket_name = 'jsonofthattree'
json_key = 'data.json'
response = s3.get_object(Bucket=bucket_name, Key=json_key)
json_data = response['Body'].read().decode('utf-8')
existing_data = json.loads(json_data)

# Update the JSON data
new_data = {'name': 'John', 'age': 30, 'city': 'New York'}
existing_data.update(new_data)

# Save the updated JSON data to S3
updated_json_data = json.dumps(existing_data)
s3.put_object(Bucket=bucket_name, Key=json_key, Body=updated_json_data)
