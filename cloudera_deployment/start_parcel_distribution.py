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
        
        # Check the status of the distribution
        distribution_id = distribution_response.get("id")
        check_distribution_status(cm_host, username, password, cluster_name, distribution_id)
        return True
    else:
        print(f"Failed to start parcel distribution. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def check_distribution_status(cm_host, username, password, cluster_name, distribution_id):
    status_url = f"{cm_host}/api/v54/clusters/{cluster_name}/parcels/products/{product}/versions/{version}/distributionStatus"
    
    while True:
        response = requests.get(status_url, auth=HTTPBasicAuth(username, password))

        if response.status_code == 200:
            status_response = response.json()
            distribution_status = status_response.get("status")
            print(f"Current distribution status: {distribution_status}")
            
            if distribution_status == "DISTRIBUTED":
                print("Parcel distribution completed successfully.")
                break
            elif distribution_status in ["DISTRIBUTION_IN_PROGRESS", "DISTRIBUTION_PENDING"]:
                print("Parcel distribution is still in progress. Waiting...")
                time.sleep(10)  # Wait for 10 seconds before checking again
            else:
                print("Parcel distribution failed.")
                break
        else:
            print(f"Failed to check distribution status. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Start Parcel Distribution')
    parser.add_argument('--cm_host', required=True, help='Cloudera Manager host URL')
    parser.add_argument('--username', required=True, help='Cloudera Manager username')
    parser.add_argument('--password', required=True, help='Cloudera Manager password')
    parser.add_argument('--cluster_name', required=True, help='Cluster name')
    parser.add_argument('--product', required=True, help='Product name')
    parser.add_argument('--version', required=True, help='Parcel version')

    args = parser.parse_args()
    start_parcel_distribution(args.cm_host, args.username, args.password, args.cluster_name, args.product, args.version)

