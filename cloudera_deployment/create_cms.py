import requests
from requests.auth import HTTPBasicAuth
import argparse
import sys
import json

def cms_exists(cm_host, username, password):
    """Check if Cloudera Management Service exists."""
    url = f"{cm_host}/api/v54/cm/service"
    response = requests.get(url, auth=HTTPBasicAuth(username, password))
    
    if response.status_code == 200:
        service = response.json().get('name', '')
        if service == 'ClouderaManagementService':
            return True
    return False

def delete_cms(cm_host, username, password):
    """Delete existing Cloudera Management Service."""
    url = f"{cm_host}/api/v54/cm/service"
    response = requests.delete(url, auth=HTTPBasicAuth(username, password))
    
    if response.status_code == 200:
        print("CMS deleted successfully.")
    else:
        print(f"Failed to delete CMS. Status code: {response.status_code}")
        print("Response:", response.text)
        sys.exit(1)

def create_cms(cm_host, username, password, hosts):
    """Create a new Cloudera Management Service."""
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

    response = requests.put(url, json=payload, auth=HTTPBasicAuth(username, password))
    
    if response.status_code == 200:
        print("Cloudera Management Service created successfully.")
        return True
    else:
        print(f"Failed to create Cloudera Management Service. Status code: {response.status_code}")
        print("Response:", response.text)
        return False

def start_cms(cm_host, username, password):
    """Start the Cloudera Management Service."""
    url = f"{cm_host}/api/v54/cm/service/commands/start"
    response = requests.post(url, auth=HTTPBasicAuth(username, password))
    
    if response.status_code == 200:
        print("Cloudera Management Service started successfully.")
    else:
        print(f"Failed to start Cloudera Management Service. Status code: {response.status_code}")
        print("Response:", response.text)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Delete, Create, and Start Cloudera Management Service')
    parser.add_argument('--cm_host', required=True, help='Cloudera Manager host URL')
    parser.add_argument('--username', required=True, help='Cloudera Manager username')
    parser.add_argument('--password', required=True, help='Cloudera Manager password')
    parser.add_argument('--hosts', required=True, nargs='+', help='List of hosts for the CMS roles')

    args = parser.parse_args()

    # Check if CMS exists
    if cms_exists(args.cm_host, args.username, args.password):
        print("Cloudera Management Service already exists. Deleting it...")
        delete_cms(args.cm_host, args.username, args.password)

    # Create the CMS
    print("Creating Cloudera Management Service...")
    if create_cms(args.cm_host, args.username, args.password, args.hosts):
        # Start the CMS
        print("Starting Cloudera Management Service...")
        start_cms(args.cm_host, args.username, args.password)

