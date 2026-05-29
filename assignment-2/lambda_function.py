import boto3
from datetime import datetime, timezone, timedelta

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    BUCKET_NAME = 'cleanup-test-bench-nagin'
    
    # FIX: Subtract 30 days to calculate the correct historical cutoff time
    cutoff_time = datetime.now(timezone.utc) - timedelta(days=30)
    
    print(f"Starting cleanup scan for bucket: '{BUCKET_NAME}' (Targeting files older than: {cutoff_time})")
    
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        
        if 'Contents' not in response:
            print(f"Bucket {BUCKET_NAME} is empty.")
            return {"status": "Bucket empty"}
            
        deleted_files = []
        for obj in response['Contents']:
            last_modified = obj['LastModified']
            
            # This evaluates if the file is older than the 30-day cutoff
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
