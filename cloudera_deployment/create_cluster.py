import requests
import json
from requests.auth import HTTPBasicAuth
import argparse
import time

def create_cluster(cm_host, username, password, cluster_name, version):
    CM_URL = f"{cm_host}/api/v54/clusters"
    cluster_payload = {
        "items": [
            {
                "name": cluster_name,
                "version": "CDH7",
                "fullVersion": version
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(
            CM_URL,
            auth=HTTPBasicAuth(username, password),
            headers=headers,
            data=json.dumps(cluster_payload)
        )
        if response.status_code in [200, 201]:
            print("Cluster created successfully.")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"Failed to create cluster. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"An error occurred while creating the cluster: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create Cloudera Cluster')
    parser.add_argument('--cm_host', required=True, help='Cloudera Manager host URL')
    parser.add_argument('--username', required=True, help='Cloudera Manager username')
    parser.add_argument('--password', required=True, help='Cloudera Manager password')
    parser.add_argument('--cluster_name', required=True, help='Cluster name')
    parser.add_argument('--version', required=True, help='CDH version')

    args = parser.parse_args()
    success = create_cluster(args.cm_host, args.username, args.password, args.cluster_name, args.version)

