import requests
import json
from requests.auth import HTTPBasicAuth
import argparse
import time

def start_parcel_download(cm_host, username, password, cluster_name, product, version):
    url = f"{cm_host}/api/v54/clusters/{cluster_name}/parcels/products/{product}/versions/{version}/commands/startDownload"
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, auth=HTTPBasicAuth(username, password), headers=headers)

    if response.status_code == 200:
        print("Parcel download started successfully.")
        download_response = response.json()
        print(json.dumps(download_response, indent=2))
        return True
    else:
        print(f"Failed to start parcel download. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def wait_for_parcel_download(cm_host, username, password, cluster_name, product, version):
    while True:
        url = f"{cm_host}/api/v54/clusters/{cluster_name}/parcels/products/{product}/versions/{version}"
        response = requests.get(url, auth=HTTPBasicAuth(username, password))

        if response.status_code == 200:
            parcel_info = response.json()
            if parcel_info.get("downloaded"):
                print("Parcel download completed.")
                return True
            else:
                print("Waiting for parcel download to complete...")
                time.sleep(10)
        else:
            print(f"Failed to get parcel status. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Start Parcel Download')
    parser.add_argument('--cm_host', required=True, help='Cloudera Manager host URL')
    parser.add_argument('--username', required=True, help='Cloudera Manager username')
    parser.add_argument('--password', required=True, help='Cloudera Manager password')
    parser.add_argument('--cluster_name', required=True, help='Cluster name')
    parser.add_argument('--product', required=True, help='Product name')
    parser.add_argument('--version', required=True, help='Parcel version')

    args = parser.parse_args()
    start_parcel_download(args.cm_host, args.username, args.password, args.cluster_name, args.product, args.version)
    wait_for_parcel_download(args.cm_host, args.username, args.password, args.cluster_name, args.product, args.version)

