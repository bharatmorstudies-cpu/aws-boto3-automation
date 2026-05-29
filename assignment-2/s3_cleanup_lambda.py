import boto3
from datetime import datetime, timedelta, timezone

# CONFIGURATION: Change this to your bucket name!
BUCKET_NAME = "cleanup-test-bench-nagin"

# TESTING MODE: Set to True to delete ALL files for testing. 
# Set to False to strictly delete files older than 30 days.
TESTING_MODE = True 

def lambda_handler(event, context):
    # 1. Initialize the S3 client
    s3 = boto3.client('s3')
    
    # Calculate the cutoff date (30 days ago from right now)
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=30)
    
    deleted_files_count = 0
    
    try:
        # 2. List objects in the specified bucket
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        
        # Check if the bucket is empty
        if 'Contents' not in response:
            print(f"Bucket '{BUCKET_NAME}' is already empty. No files to clean up.")
            return {'statusCode': 200, 'body': 'No files found to clean up.'}
            
        print(f"Scanning bucket: {BUCKET_NAME}...")
        
        # 3. Iterate through objects and evaluate age
        for obj in response['Contents']:
            file_name = obj['Key']
            file_modified_time = obj['LastModified'] # This is timezone-aware
            
            # Deletion conditions
            should_delete = False
            if TESTING_MODE:
                should_delete = True
                reason = "Testing Mode is ENABLED (deletes all files)"
            elif file_modified_time < cutoff_date:
                should_delete = True
                reason = f"File age is older than 30 days (Modified: {file_modified_time})"
                
            if should_delete:
                # Delete the object
                s3.delete_object(Bucket=BUCKET_NAME, Key=file_name)
                # 4. Print the names of deleted objects for logging purposes
                print(f"SUCCESSFULLY DELETED: {file_name} | Reason: {reason}")
                deleted_files_count += 1
                
        return {
            'statusCode': 200,
            'body': f"Cleanup completed. Total files deleted: {deleted_files_count}"
        }
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"Error executing cleanup: {str(e)}"
        }
