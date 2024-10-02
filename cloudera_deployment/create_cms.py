import requests
import json
import argparse
from requests.auth import HTTPBasicAuth
import time

def create_cms(cm_host, username, password, hosts):
    url = f"{cm_host}/api/v54/cm/service"
    headers = {
        "Content-Type": "application/json"
    }

    # Prepare the request body
    data = {
        "type": "MGMT",
        "name": "ClouderaManagementService",
        "roles": [
            {"type": "SERVICEMONITOR", "hostRef": {"hostId": hosts[0]}},  # You can modify this to use any host from the list
            {"type": "HOSTMONITOR", "hostRef": {"hostId": hosts[0]}},
            {"type": "EVENTSERVER", "hostRef": {"hostId": hosts[0]}},
            {"type": "ALERTPUBLISHER", "hostRef": {"hostId": hosts[0]}}
        ]
    }

    response = requests.put(url, auth=HTTPBasicAuth(username, password), headers=headers, data=json.dumps(data))

    if response.status_code in [200, 201]:
        print("Cloudera Management Service created successfully.")
        print(json.dumps(response.json(), indent=2))
        return True
    else:
        print(f"Failed to create Cloudera Management Service. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def start_cms(cm_host, username, password):
    url = f"{cm_host}/api/v54/cm/service/ClouderaManagementService/command/start"
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, auth=HTTPBasicAuth(username, password), headers=headers)

    if response.status_code in [200, 201]:
        print("Cloudera Management Service started successfully.")
        return True
    else:
        print(f"Failed to start Cloudera Management Service. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create and Start Cloudera Management Service')
    parser.add_argument('--cm_host', required=True, help='Cloudera Manager host URL')
    parser.add_argument('--username', required=True, help='Cloudera Manager username')
    parser.add_argument('--password', required=True, help='Cloudera Manager password')
    parser.add_argument('--hosts', required=True, nargs='+', help='List of hosts for the CMS roles')

    args = parser.parse_args()

    if create_cms(args.cm_host, args.username, args.password, args.hosts):
        # Start the CMS after successful creation
        start_cms(args.cm_host, args.username, args.password)

