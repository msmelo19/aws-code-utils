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

instance_id = check_spot_instance_termination()
if instance_id:
    print("A instância " + instance_id + " está programada para ser interrompida.")