import requests
import json
from requests.auth import HTTPBasicAuth

# Load configuration from config.json
with open('config.json') as config_file:
    config = json.load(config_file)

CM_URL = f"{config['cm_host']}/api/v54/clusters"
USERNAME = config['username']
PASSWORD = config['password']

# Cluster creation payload
cluster_payload = {
    "items": [
        {
            "name": config['cluster_name'],
            "version": "CDH7",
            "fullVersion": config['version']
        }
    ]
}

# Function to create the cluster
def create_cluster():
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(
            CM_URL,
            auth=HTTPBasicAuth(USERNAME, PASSWORD),
            headers=headers,
            data=json.dumps(cluster_payload)
        )
        if response.status_code in [200, 201]:
            print("Cluster created successfully.")
            print(f"Response: {response.json()}")
        else:
            print(f"Failed to create cluster. Status code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"An error occurred while creating the cluster: {e}")

# Call the function to create the cluster
create_cluster()

