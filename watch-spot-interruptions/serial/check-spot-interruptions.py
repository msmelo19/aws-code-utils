import boto3

def check_spot_instance_termination(instance_id):
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances(InstanceIds=[instance_id])
    instances = response['Reservations'][0]['Instances']
    
    if len(instances) > 0:
        instance = instances[0]
        if 'SpotInstanceRequestId' in instance:
            spot_request_id = instance['SpotInstanceRequestId']
            response = ec2.describe_spot_instance_requests(SpotInstanceRequestIds=[spot_request_id])
            spot_instance_request = response['SpotInstanceRequests'][0]
            
            if spot_instance_request['Status']['Code'] == 'marked-for-termination' \
            or spot_instance_request['Status']['Code'] == 'marked-for-stop' \
            or spot_instance_request['Status']['Code'] == 'instance-terminated-by-experiment' \
            or spot_instance_request['Status']['Code'] == 'marked-for-stop-by-experiment':
                return True
    
    return False

instance_id = 'i-051f582ad3f153d71'
is_termination_scheduled = check_spot_instance_termination(instance_id)
if is_termination_scheduled:
    print("A instância está programada para ser interrompida.")
else:
    print("A instância não está programada para ser interrompida.")
