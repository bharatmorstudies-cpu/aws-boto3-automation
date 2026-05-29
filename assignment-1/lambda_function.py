import boto3

def lambda_handler(event, context):
    # Connect to the EC2 service in Stockholm region
    ec2 = boto3.client('ec2', region_name='eu-north-1')
    
    # 1. Find and STOP running instances tagged with Action=Auto-Stop
    stop_filter = [
        {'Name': 'tag:Action', 'Values': ['Auto-Stop']},
        {'Name': 'instance-state-name', 'Values': ['running']}
    ]
    instances_to_stop = ec2.describe_instances(Filters=stop_filter)
    stop_ids = [i['InstanceId'] for r in instances_to_stop['Reservations'] for i in r['Instances']]
    
    if stop_ids:
        print(f"Stopping instances: {stop_ids}")
        ec2.stop_instances(InstanceIds=stop_ids)
    else:
        print("No running 'Auto-Stop' instances found.")

    # 2. Find and START stopped instances tagged with Action=Auto-Start
    start_filter = [
        {'Name': 'tag:Action', 'Values': ['Auto-Start']},
        {'Name': 'instance-state-name', 'Values': ['stopped']}
    ]
    instances_to_start = ec2.describe_instances(Filters=start_filter)
    start_ids = [i['InstanceId'] for r in instances_to_start['Reservations'] for i in r['Instances']]
    
    if start_ids:
        print(f"Starting instances: {start_ids}")
        ec2.start_instances(InstanceIds=start_ids)
    else:
        print("No stopped 'Auto-Start' instances found.")

# THIS IS CRITICAL FOR POWERSHELL: This line must be at the very bottom
if __name__ == "__main__":
    lambda_handler({}, None)
