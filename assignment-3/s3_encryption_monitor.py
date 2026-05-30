import boto3
from botocore.exceptions import ClientError

# CONFIGURATION: Set the bucket name to match your active target architecture
BUCKET_NAME = "cleanup-test-bench-nagin"

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    print(f"Initiating security compliance audit for target bucket: '{BUCKET_NAME}'...")
    
    try:
        # Retrieve the server-side encryption configuration
        encryption_status = s3.get_bucket_encryption(Bucket=BUCKET_NAME)
        rules = encryption_status.get('ServerSideEncryptionConfiguration', {}).get('Rules', [])
        
        print(" [COMPLIANT] Server-Side Encryption (SSE) is ENABLED.")
        for rule in rules:
            sse_algorithm = rule.get('ApplyServerSideEncryptionByDefault', {}).get('SSEAlgorithm')
            print(f" -> Encryption Mechanism Algorithm: {sse_algorithm}")
            
        return {
            'statusCode': 200,
            'complianceStatus': 'COMPLIANT',
            'bucketChecked': BUCKET_NAME,
            'algorithm': sse_algorithm
        }
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        
        # This explicit exception catches when default encryption is disabled or missing
        if error_code == 'ServerSideEncryptionConfigurationNotFoundError':
            print(f" [NON-COMPLIANT ALERT] Bucket '{BUCKET_NAME}' does not have Server-Side Encryption enabled!")
            return {
                'statusCode': 200,
                'complianceStatus': 'NON-COMPLIANT',
                'bucketChecked': BUCKET_NAME,
                'error': 'Encryption configuration missing'
            }
        else:
            print(f"An unexpected API access validation exception occurred: {str(e)}")
            return {
                'statusCode': 500,
                'body': f"Error evaluating encryption status: {str(e)}"
            }
