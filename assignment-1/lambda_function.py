import boto3

def lambda_handler(event, context):
    # Initialize the EC2 client
    ec2 = boto3.client('ec2')
    
    # 1. Find and stop instances with tag Action=Auto-Stop
    stop_filter = [{'Name': 'tag:Action', 'Values': ['Auto-Stop']}]
    instances_to_stop = ec2.describe_instances(Filters=stop_filter)
    
    stop_ids = []
    for reservation in instances_to_stop['Reservations']:
        for instance in reservation['Instances']:
            # Avoid stopping already stopped instances
            if instance['State']['Name'] == 'running':
                stop_ids.append(instance['InstanceId'])
                
    if stop_ids:
        ec2.stop_instances(InstanceIds=stop_ids)
        print(f"Successfully stopped instances: {stop_ids}")
    else:
        print("No running instances found with tag 'Action=Auto-Stop'.")

    # 2. Find and start instances with tag Action=Auto-Start
    start_filter = [{'Name': 'tag:Action', 'Values': ['Auto-Start']}]
    instances_to_start = ec2.describe_instances(Filters=start_filter)
    
    start_ids = []
    for reservation in instances_to_start['Reservations']:
        for instance in reservation['Instances']:
            # Avoid starting already running instances
            if instance['State']['Name'] == 'stopped':
                start_ids.append(instance['InstanceId'])
                
    if start_ids:
        ec2.start_instances(InstanceIds=start_ids)
        print(f"Successfully started instances: {start_ids}")
    else:
        print("No stopped instances found with tag 'Action=Auto-Start'.")
        
    return {
        'statusCode': 200,
        'body': 'EC2 automation execution completed successfully!'
    }
