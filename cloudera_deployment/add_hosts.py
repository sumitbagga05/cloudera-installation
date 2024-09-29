import requests
import json
from requests.auth import HTTPBasicAuth
import argparse
import time

def add_hosts_to_cluster(cm_host, username, password, cluster_name, hostnames):
    url = f"{cm_host}/api/v54/clusters/{cluster_name}/hosts"
    headers = {'Content-Type': 'application/json'}

    data = {
        "items": [{"hostId": hostname} for hostname in hostnames]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data), auth=(username, password))

    if response.status_code == 200:
        print("Hosts added successfully.")
        return True
    else:
        print(f"Failed to add hosts. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Add Hosts to Cloudera Cluster')
    parser.add_argument('--cm_host', required=True, help='Cloudera Manager host URL')
    parser.add_argument('--username', required=True, help='Cloudera Manager username')
    parser.add_argument('--password', required=True, help='Cloudera Manager password')
    parser.add_argument('--cluster_name', required=True, help='Cluster name')
    parser.add_argument('--hosts', required=True, nargs='+', help='List of hosts to add to the cluster')

    args = parser.parse_args()
    success = add_hosts_to_cluster(args.cm_host, args.username, args.password, args.cluster_name, args.hosts)

