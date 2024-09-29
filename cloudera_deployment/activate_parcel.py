import requests
import json
from requests.auth import HTTPBasicAuth
import argparse
import time

def activate_parcel(cm_host, username, password, cluster_name, product, version):
    url = f"{cm_host}/api/v54/clusters/{cluster_name}/parcels/products/{product}/versions/{version}/commands/activate"
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, auth=HTTPBasicAuth(username, password), headers=headers)

    if response.status_code == 200:
        activation_response = response.json()
        if activation_response.get("success"):
            print("Parcel activation started successfully.")
            return True
        else:
            print("Parcel activation failed.")
            print(json.dumps(activation_response, indent=2))
            return False
    else:
        print(f"Failed to activate parcel. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def check_parcel_status(cm_host, username, password, cluster_name, product, version):
    url = f"{cm_host}/api/v54/clusters/{cluster_name}/parcels/products/{product}/versions/{version}"
    response = requests.get(url, auth=HTTPBasicAuth(username, password))

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get parcel status. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def wait_for_parcel_activation(cm_host, username, password, cluster_name, product, version):
    while True:
        parcel_info = check_parcel_status(cm_host, username, password, cluster_name, product, version)
        
        if parcel_info:
            stage = parcel_info.get("stage")
            activated = parcel_info.get("activated", False)  # Default to False if not present

            # Debugging logs to verify what is being received
            print(f"Parcel stage: {stage}")
            print(f"Parcel activated: {activated}")

            if stage == "ACTIVATED" and activated:
                print("Parcel activation completed successfully.")
                print(json.dumps(parcel_info, indent=2))
                return True
            elif stage == "ACTIVATING":
                print(f"Parcel is still activating. Progress: {parcel_info.get('state', {}).get('progress', 0)}%")
            else:
                print(f"Unexpected stage: {stage}. Continuing to wait...")

        time.sleep(10)  # Wait before checking the status again

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Activate Parcel')
    parser.add_argument('--cm_host', required=True, help='Cloudera Manager host URL')
    parser.add_argument('--username', required=True, help='Cloudera Manager username')
    parser.add_argument('--password', required=True, help='Cloudera Manager password')
    parser.add_argument('--cluster_name', required=True, help='Cluster name')
    parser.add_argument('--product', required=True, help='Product name')
    parser.add_argument('--version', required=True, help='Parcel version')

    args = parser.parse_args()

    if activate_parcel(args.cm_host, args.username, args.password, args.cluster_name, args.product, args.version):
        wait_for_parcel_activation(args.cm_host, args.username, args.password, args.cluster_name, args.product, args.version)

