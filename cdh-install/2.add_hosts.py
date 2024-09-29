import requests
import json

# Load configuration from config.json
with open('config.json') as config_file:
    config = json.load(config_file)

CM_HOST = config['cm_host']
USERNAME = config['username']
PASSWORD = config['password']
CLUSTER_NAME = config['cluster_name']

# Set the API endpoint for adding hosts to the cluster
API_VERSION = "v54"  
url = f"{CM_HOST}/api/{API_VERSION}/clusters/{CLUSTER_NAME}/hosts"
HEADERS = {'Content-Type': 'application/json'}

# Function to add hosts to the cluster
def add_hosts_to_cluster(hostnames):
    data = {
        "items": [{"hostId": hostname} for hostname in hostnames]
    }

    # Send the POST request to add hosts
    response = requests.post(url, headers=HEADERS, data=json.dumps(data), auth=(USERNAME, PASSWORD))

    if response.status_code == 200:
        return response.json()  
    else:
        return {"error": response.status_code, "message": response.text}

# Example usage
if __name__ == "__main__":
    hostnames = config['hosts']  # Use hostnames from config

    print("Adding hosts to the cluster...")
    add_hosts_response = add_hosts_to_cluster(hostnames)
    print(json.dumps(add_hosts_response, indent=4))

