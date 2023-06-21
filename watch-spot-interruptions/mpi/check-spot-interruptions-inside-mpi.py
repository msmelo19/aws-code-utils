from mpi4py import MPI
import requests
from time import sleep

def check_spot_instance_termination():
    while True:
        try:
            res = requests.head('http://169.254.169.254/latest/meta-data/spot/instance-action')
            
            if(res.status_code == 200):
                return requests.get('http://169.254.169.254/latest/meta-data/instance-id').text
            else:
                sleep(10)
                
        except Exception as e:
            print(e)
            return

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
    for i in range(1, size):
        instance_id = comm.recv(source=i)
        print("A instância " + instance_id + " está programada para ser interrompida.")
else:
    is_termination_scheduled = check_spot_instance_termination()
    comm.send(is_termination_scheduled, dest=0)