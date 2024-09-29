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

def wait_for_parcel_download(cm_host, username, password, cluster_name, product, version, timeout=600, interval=10):
    elapsed_time = 0
    while elapsed_time < timeout:
        url = f"{cm_host}/api/v54/clusters/{cluster_name}/parcels/products/{product}/versions/{version}"
        response = requests.get(url, auth=HTTPBasicAuth(username, password))

        if response.status_code == 200:
            parcel_info = response.json()
            stage = parcel_info.get("stage")
            
            if stage == "DOWNLOADED":
                print("Parcel download completed successfully.")
                print(json.dumps(parcel_info, indent=2))
                return True
            elif stage == "DOWNLOADING":
                progress = parcel_info.get('state', {}).get('progress', 0)
                print(f"Parcel is still downloading. Current progress: {progress}%")
            else:
                print(f"Unexpected status: {stage}")
        else:
            print(f"Failed to get parcel status. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False

        time.sleep(interval)
        elapsed_time += interval

    # Timeout reached
    print(f"Timeout reached after {timeout} seconds. Parcel download did not complete.")
    return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Start and Monitor Parcel Download')
    parser.add_argument('--cm_host', required=True, help='Cloudera Manager host URL')
    parser.add_argument('--username', required=True, help='Cloudera Manager username')
    parser.add_argument('--password', required=True, help='Cloudera Manager password')
    parser.add_argument('--cluster_name', required=True, help='Cluster name')
    parser.add_argument('--product', required=True, help='Product name')
    parser.add_argument('--version', required=True, help='Parcel version')

    args = parser.parse_args()

    if start_parcel_download(args.cm_host, args.username, args.password, args.cluster_name, args.product, args.version):
        wait_for_parcel_download(args.cm_host, args.username, args.password, args.cluster_name, args.product, args.version)

