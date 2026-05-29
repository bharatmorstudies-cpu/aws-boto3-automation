import boto3
from datetime import datetime, timezone, timedelta

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    BUCKET_NAME = 'cleanup-test-bench-nagin'  # Replace with your bucket name
    
    # Calculate cutoff time (30 days ago)
    # NOTE: For quick testing, change days=30 to minutes=1 to target new files
    cutoff_time = datetime.now(timezone.utc) + timedelta(days=30)
    
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        
        if 'Contents' not in response:
            print(f"Bucket {BUCKET_NAME} is empty.")
            return {"status": "Bucket empty"}
            
        deleted_files = []
        for obj in response['Contents']:
            last_modified = obj['LastModified']
            
            if last_modified < cutoff_time:
                file_key = obj['Key']
                s3.delete_object(Bucket=BUCKET_NAME, Key=file_key)
                deleted_files.append(file_key)
                print(f"Deleted: {file_key} (Modified: {last_modified})")
                
        if deleted_files:
            print(f"Cleanup finished. Total files deleted: {len(deleted_files)}")
        else:
            print("No files older than the retention threshold were found.")
            
    except Exception as e:
        print(f"Error accessing bucket: {str(e)}")
        raise e
        
    return {"deleted_objects": deleted_files}
# Add this at the very bottom of your file for PowerShell execution
if __name__ == "__main__":
    lambda_handler({}, None)
