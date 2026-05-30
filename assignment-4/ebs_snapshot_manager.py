import boto3
from datetime import datetime, timedelta, timezone

# CONFIGURATION: Replace with an active EBS Volume ID from your EC2 Dashboard
VOLUME_ID = "vol-05cd2fb7f521e211e"  

# TESTING MODE: Set to True to instantly delete the newly created snapshot for testing.
# Set to False to strictly clean up snapshots older than 30 days.
TESTING_MODE = True

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    print(f"Initiating EBS automation for Volume ID: {VOLUME_ID}")
    
    # 1. Create a snapshot for the specified EBS volume
    try:
        description = f"Automated backup for {VOLUME_ID} created on {datetime.now().strftime('%Y-%m-%d')}"
        snapshot = ec2.create_snapshot(
            VolumeId=VOLUME_ID,
            Description=description,
            TagSpecifications=[
                {
                    'ResourceType': 'snapshot',
                    'Tags': [{'Key': 'CreatedBy', 'Value': 'Lambda-EBS-Manager'}]
                }
            ]
        )
        new_snapshot_id = snapshot['SnapshotId']
        print(f"SUCCESSFULLY CREATED SNAPSHOT: {new_snapshot_id} for Volume {VOLUME_ID}")
    except Exception as e:
        print(f"Error creating snapshot: {str(e)}")
        return {'statusCode': 500, 'body': f"Snapshot creation failed: {str(e)}"}

    # 2. Calculate the cutoff date (30 days ago)
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=30)
    deleted_snapshots_count = 0

    try:
        # 3. List snapshots created by this automation account filter
        response = ec2.describe_snapshots(
            Filters=[
                {'Name': 'volume-id', 'Values': [VOLUME_ID]},
                {'Name': 'tag:CreatedBy', 'Values': ['Lambda-EBS-Manager']}
            ]
        )
        
        # 4. Iterate through snapshots and evaluate age constraints
        for snap in response['Snapshots']:
            snap_id = snap['SnapshotId']
            snap_time = snap['StartTime']  # Timezone-aware timestamp
            
            should_delete = False
            if TESTING_MODE:
                # If testing, target the snapshot we just created to prove deletion works
                if snap_id == new_snapshot_id:
                    should_delete = True
                    reason = "Testing Mode is ENABLED (Instantly cleaning test asset)"
            elif snap_time < cutoff_date:
                should_delete = True
                reason = f"Snapshot age exceeds 30-day retention policy (Created: {snap_time})"

            if should_delete:
                ec2.delete_snapshot(SnapshotId=snap_id)
                print(f"SUCCESSFULLY DELETED SNAPSHOT: {snap_id} | Reason: {reason}")
                deleted_snapshots_count += 1

        return {
            'statusCode': 200,
            'body': f"EBS backup completed. Created: {new_snapshot_id}. Purged {deleted_snapshots_count} snapshots."
        }
    except Exception as e:
        print(f"Error executing cleanup cycle: {str(e)}")
        return {'statusCode': 500, 'body': f"Cleanup cycle encountered errors: {str(e)}"}
