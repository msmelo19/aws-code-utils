from mpi4py import MPI
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

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
    for i in range(1, size):
        result = comm.recv(source=i)
else:
    is_termination_scheduled = check_spot_instance_termination()
    comm.send(is_termination_scheduled, dest=0)