import subprocess
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Main Cloudera Deployment Orchestration')
    parser.add_argument('--cm_host', required=True, help='Cloudera Manager host URL')
    parser.add_argument('--username', required=True, help='Cloudera Manager username')
    parser.add_argument('--password', required=True, help='Cloudera Manager password')
    parser.add_argument('--cluster_name', required=True, help='Cluster name')
    parser.add_argument('--version', required=True, help='CDH version')
    parser.add_argument('--hosts', required=True, nargs='+', help='List of hosts to add to the cluster')
    parser.add_argument('--product', required=True, help='Product name')
    
    args = parser.parse_args()

    # Step 1: Create Cluster
    subprocess.run(["python3", "cloudera_deployment/create_cluster.py", "--cm_host", args.cm_host,
                    "--username", args.username, "--password", args.password,
                    "--cluster_name", args.cluster_name, "--version", args.version])

    # Step 2: Add Hosts
    subprocess.run(["python3", "cloudera_deployment/add_hosts.py", "--cm_host", args.cm_host,
                    "--username", args.username, "--password", args.password,
                    "--cluster_name", args.cluster_name, "--hosts"] + args.hosts)

    # Step 3: Start Parcel Download
    subprocess.run(["python3", "cloudera_deployment/start_parcel_download.py", "--cm_host", args.cm_host,
                    "--username", args.username, "--password", args.password,
                    "--cluster_name", args.cluster_name, "--product", args.product,
                    "--version", args.version])

    # Step 4: Start Parcel Distribution
    subprocess.run(["python3", "cloudera_deployment/start_parcel_distribution.py", "--cm_host", args.cm_host,
                    "--username", args.username, "--password", args.password,
                    "--cluster_name", args.cluster_name, "--product", args.product,
                    "--version", args.version])

    # Step 5: Activate Parcel
    subprocess.run(["python3", "cloudera_deployment/activate_parcel.py", "--cm_host", args.cm_host,
                    "--username", args.username, "--password", args.password,
                    "--cluster_name", args.cluster_name, "--product", args.product,
                    "--version", args.version])

