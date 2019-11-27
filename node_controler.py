import requests
from pprint import pprint

if __name__ == '__main__':
    is_running = True
    node_address = input("Please enter the IPv4:port of your node \n >")
    while is_running:
        requests.get('http://' + node_address + '/nodes/resolve')
        command = input(">")
        if command == 'mine':
            print('Mining...')
            response = requests.get('http://' + node_address + '/mine')
            if response.status_code == 200:
                pprint(response.json())
                requests.get('http://' + node_address + '/nodes/resolve')
        elif command == 'new-node':
            new_node_address = input("Enter the IPv4:port of the node that you want to add in the node list \n >")
            response = requests.post('http://'+node_address+'/nodes/register', {'nodes': 'http://'+new_node_address})
            if response.status_code == 201:
                pprint(response.json())
            else:
                pprint(response)
        elif command == 'chain':
            response = requests.get('http://' + node_address + '/chain')
            if response.status_code == 200:
                pprint(response.json())
        elif command == "transactions":
            response = requests.get('http://' + node_address + '/transactions/get')
            if response.status_code == 200:
                pprint(response.json())
        elif command == 'exit':
            is_running = False
