import requests
from requests.auth import HTTPBasicAuth
import argparse

def cms_exists(cm_host, username, password):
    url = f"{cm_host}/api/v54/cm/service/ClouderaManagementService"
    response = requests.get(url, auth=HTTPBasicAuth(username, password))
    return response.status_code == 200

def delete_cms(cm_host, username, password):
    url = f"{cm_host}/api/v54/cm/service/ClouderaManagementService"
    response = requests.delete(url, auth=HTTPBasicAuth(username, password))
    return response

def start_cms(cm_host, username, password):
    url = f"{cm_host}/api/v54/cm/service/ClouderaManagementService/start"
    response = requests.put(url, auth=HTTPBasicAuth(username, password))
    return response.status_code == 200

def create_cms(cm_host, username, password, hosts):
    url = f"{cm_host}/api/v54/cm/service"
    payload = {
        "type": "MGMT",
        "name": "ClouderaManagementService",
        "roles": [
            {"type": "SERVICEMONITOR", "hostRef": {"hostId": hosts[0]}},
            {"type": "HOSTMONITOR", "hostRef": {"hostId": hosts[0]}},
            {"type": "EVENTSERVER", "hostRef": {"hostId": hosts[0]}},
            {"type": "ALERTPUBLISHER", "hostRef": {"hostId": hosts[0]}}
        ]
    }
    
    response = requests.post(url, json=payload, auth=HTTPBasicAuth(username, password))
    return response

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Delete, Create and Start Cloudera Management Service')
    parser.add_argument('--cm_host', required=True, help='Cloudera Manager host URL')
    parser.add_argument('--username', required=True, help='Cloudera Manager username')
    parser.add_argument('--password', required=True, help='Cloudera Manager password')
    parser.add_argument('--hosts', required=True, nargs='+', help='List of hosts for the CMS roles')

    args = parser.parse_args()

    if cms_exists(args.cm_host, args.username, args.password):
        print("Cloudera Management Service already exists. Deleting it...")
        delete_response = delete_cms(args.cm_host, args.username, args.password)
        
        if delete_response.status_code == 200:
            print("CMS deleted successfully.")
        else:
            print("Failed to delete CMS. Please check the logs for more details.")
            print(f"Response: {delete_response.json()}")
            exit(1)

    print("Creating Cloudera Management Service...")
    create_response = create_cms(args.cm_host, args.username, args.password, args.hosts)

    if create_response.status_code == 201:  # 201 Created
        print("Cloudera Management Service created successfully.")
        
        # Start the CMS after successful creation
        if start_cms(args.cm_host, args.username, args.password):
            print("CMS started successfully.")
        else:
            print("Failed to start the CMS after creation. Please check the logs for more details.")
    else:
        print(f"Failed to create Cloudera Management Service. Status code: {create_response.status_code}")
        print("Response:", create_response.json())

