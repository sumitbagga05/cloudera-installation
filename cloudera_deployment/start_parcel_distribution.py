import requests
import json
from requests.auth import HTTPBasicAuth
import argparse
import time

def start_parcel_distribution(cm_host, username, password, cluster_name, product, version):
    url = f"{cm_host}/api/v54/clusters/{cluster_name}/parcels/products/{product}/versions/{version}/commands/startDistribution"
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, auth=HTTPBasicAuth(username, password), headers=headers)

    if response.status_code == 200:
        print("Parcel distribution started successfully.")
        distribution_response = response.json()
        print(json.dumps(distribution_response, indent=2))
        return True
    else:
        print(f"Failed to start parcel distribution. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def check_parcel_status(cm_host, username, password, cluster_name, product, version):
    url = f"{cm_host}/api/v54/clusters/{cluster_name}/parcels/products/{product}/versions/{version}"
    response = requests.get(url, auth=HTTPBasicAuth(username, password))

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to check parcel status. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def wait_for_parcel_distribution(cm_host, username, password, cluster_name, product, version, timeout=600, interval=10):
    elapsed_time = 0
    while elapsed_time < timeout:
        status = check_parcel_status(cm_host, username, password, cluster_name, product, version)
        if status:
            stage = status.get("stage")
            if stage == "DISTRIBUTED":
                print("Parcel distribution completed successfully.")
                print(json.dumps(status, indent=2))
                return True
            elif stage == "DISTRIBUTING":
                progress = status.get('state', {}).get('progress', 0)
                print(f"Parcel is still distributing. Current progress: {progress}%")
            else:
                print(f"Unexpected status: {stage}")
        else:
            print("Unable to retrieve parcel status.")

        time.sleep(interval)
        elapsed_time += interval

    # Timeout reached
    print(f"Timeout reached after {timeout} seconds. Parcel distribution did not complete.")
    return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Start and Monitor Parcel Distribution')
    parser.add_argument('--cm_host', required=True, help='Cloudera Manager host URL')
    parser.add_argument('--username', required=True, help='Cloudera Manager username')
    parser.add_argument('--password', required=True, help='Cloudera Manager password')
    parser.add_argument('--cluster_name', required=True, help='Cluster name')
    parser.add_argument('--product', required=True, help='Product name (e.g., CDH)')
    parser.add_argument('--version', required=True, help='Parcel version (e.g., 6.3.2)')

    args = parser.parse_args()

    if start_parcel_distribution(args.cm_host, args.username, args.password, args.cluster_name, args.product, args.version):
        wait_for_parcel_distribution(args.cm_host, args.username, args.password, args.cluster_name, args.product, args.version)

