import os
import json
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

def create_minio_bucket():
    """
    Create the MinIO bucket if it doesn't exist
    """
    try:
        # MinIO settings from environment variables
        access_key = os.getenv('MINIO_ACCESS_KEY')
        secret_key = os.getenv('MINIO_SECRET_KEY')
        endpoint_url = f"http://{os.getenv('MINIO_ENDPOINT')}"
        bucket_name = os.getenv('MINIO_BUCKET_NAME')
        # Безопасное значение по умолчанию для MINIO_SECURE
        secure = os.getenv('MINIO_SECURE', '0') == '1'
        
        print(f"Connecting to MinIO at {endpoint_url}")
        
        # Create S3 client
        s3_client = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            config=Config(signature_version='s3v4'),
            verify=secure
        )
        
        # Check if bucket exists
        try:
            s3_client.head_bucket(Bucket=bucket_name)
            print(f"Bucket '{bucket_name}' already exists")
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                # Bucket doesn't exist, create it
                s3_client.create_bucket(Bucket=bucket_name)
                print(f"Created bucket '{bucket_name}'")
                
                # Set bucket policy to make it publicly readable
                bucket_policy = {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Sid": "PublicReadGetObject",
                            "Effect": "Allow",
                            "Principal": "*",
                            "Action": ["s3:GetObject"],
                            "Resource": [f"arn:aws:s3:::{bucket_name}/*"]
                        }
                    ]
                }
                s3_client.put_bucket_policy(
                    Bucket=bucket_name,
                    Policy=json.dumps(bucket_policy)  # Безопасная сериализация JSON
                )
                print(f"Set public-read policy on bucket '{bucket_name}'")
            else:
                print(f"Error checking bucket: {e}")
                raise
                
        return True
    except Exception as e:
        print(f"Failed to initialize MinIO bucket: {e}")
        return False

if __name__ == "__main__":
    print("Initializing MinIO bucket...")
    create_minio_bucket()