import requests
from requests.auth import HTTPBasicAuth
import json
import time

# Load configuration from config.json
with open('config.json') as config_file:
    config = json.load(config_file)

CM_HOST = config['cm_host']
CLUSTER_NAME = config['cluster_name']
PRODUCT = "CDH"
VERSION = config['version']
USERNAME = config['username']
PASSWORD = config['password']

def start_parcel_distribution():
    url = f"{CM_HOST}/api/v54/clusters/{CLUSTER_NAME}/parcels/products/{PRODUCT}/versions/{VERSION}/commands/startDistribution"
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, auth=HTTPBasicAuth(USERNAME, PASSWORD), headers=headers)

    if response.status_code == 200:
        print("Parcel distribution started successfully.")
        distribution_response = response.json()
        print(json.dumps(distribution_response, indent=2))
        return True
    else:
        print(f"Failed to start parcel distribution. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def check_parcel_status():
    url = f"{CM_HOST}/api/v54/clusters/{CLUSTER_NAME}/parcels/products/{PRODUCT}/versions/{VERSION}"
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD), headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to check parcel status. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def wait_for_distribution():
    while True:
        status = check_parcel_status()
        if status:
            stage = status.get("stage")
            if stage == "DISTRIBUTED":
                print("Parcel distribution completed successfully.")
                print(json.dumps(status, indent=2))
                break
            elif stage == "DISTRIBUTING":
                print("Parcel is still distributing. Current progress:", status['state']['progress'], "%")
            else:
                print("Unexpected status:", stage)

        time.sleep(10)  # Wait before checking the status again

if __name__ == "__main__":
    if start_parcel_distribution():  # Start distribution
        wait_for_distribution()  # Wait for distribution to complete

