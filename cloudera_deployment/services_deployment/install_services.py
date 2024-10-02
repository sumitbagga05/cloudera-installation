import subprocess
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Install Services on Cloudera Cluster')
    parser.add_argument('--cm_host', required=True, help='Cloudera Manager host URL')
    parser.add_argument('--username', required=True, help='Cloudera Manager username')
    parser.add_argument('--password', required=True, help='Cloudera Manager password')
    parser.add_argument('--cluster_name', required=True, help='Cluster name')
    parser.add_argument('--hosts', required=True, nargs='+', help='List of hosts')
    parser.add_argument('--services', required=True, help='Comma-separated list of services to install')

    args = parser.parse_args()

    services = args.services.split(',')

    for service in services:
        # Add logic for installing each service using Cloudera Manager API or CLI
        subprocess.run([
            "python3", f"cloudera_deployment/install_{service.lower()}.py",
            "--cm_host", args.cm_host,
            "--username", args.username,
            "--password", args.password,
            "--cluster_name", args.cluster_name,
            "--hosts"] + args.hosts)

