#!/bin/bash

# Cloudera Manager Version (choose appropriate version, this is an example for 7.6.1)
CM_VERSION="7.11.3.11"

# CM Repository for Cloudera Manager packages (use provided URL)
CM_REPO_URL="https://a4bb8d9a-4f9b-457b-afc1-e9518d1713bc:c6c0b4c7799f@archive.cloudera.com/cm7/${CM_VERSION}/redhat8/yum/cloudera-manager.repo"

# PostgreSQL version
PG_VERSION="16"

# Cloudera Manager and related services installation
install_cloudera_manager() {
    # 1. Install Java (OpenJDK 1.8.0)
    echo "Installing Java..."
    yum update -y
    yum install -y java-1.8.0-openjdk-devel

    # 2. Add Cloudera Manager repository
    echo "Adding Cloudera Manager repository..."
    wget $CM_REPO_URL -O /etc/yum.repos.d/cloudera-manager.repo

    # 3. Install Cloudera Manager Server, Agent, and Daemons
    echo "Installing Cloudera Manager Server and Agent..."
    yum install -y cloudera-manager-server cloudera-manager-agent cloudera-manager-daemons

    # 4. Install PostgreSQL (use version 16 in this case)
    echo "Installing PostgreSQL ${PG_VERSION}..."
    yum install -y postgresql-server
    
    # 5. Initialize and start PostgreSQL
    echo "Initializing and starting PostgreSQL..."
    postgresql-setup initdb
    systemctl start postgresql
    systemctl enable postgresql

    # 6. Set PostgreSQL to listen on all interfaces
    echo "Configuring PostgreSQL to listen on all interfaces..."
    cp pg_hba.conf /var/lib/pgsql/data/pg_hba.conf
    cp postgresql.conf /var/lib/pgsql/data/postgresql.conf

    # 7. Restart PostgreSQL to apply changes
    systemctl restart postgresql

    # 8. Create PostgreSQL users and databases for Cloudera Manager
    echo "Creating PostgreSQL users and databases for Cloudera Manager..."
    sudo -u postgres psql <<EOF
CREATE ROLE scm LOGIN PASSWORD 'scm_password';
CREATE ROLE amon LOGIN PASSWORD 'amon_password';
CREATE ROLE rman LOGIN PASSWORD 'rman_password';
CREATE ROLE hive LOGIN PASSWORD 'hive_password';
CREATE ROLE sentry LOGIN PASSWORD 'sentry_password';
CREATE ROLE nav LOGIN PASSWORD 'nav_password';
CREATE ROLE navms LOGIN PASSWORD 'navms_password';
CREATE ROLE hue LOGIN PASSWORD 'hue_password';
CREATE ROLE oozie LOGIN PASSWORD 'oozie_password';
CREATE DATABASE scm OWNER scm ENCODING 'UTF8';
CREATE DATABASE amon OWNER amon ENCODING 'UTF8';
CREATE DATABASE rman OWNER rman ENCODING 'UTF8';
CREATE DATABASE metastore OWNER hive ENCODING 'UTF8';
CREATE DATABASE sentry OWNER sentry ENCODING 'UTF8';
CREATE DATABASE nav OWNER nav ENCODING 'UTF8';
CREATE DATABASE navms OWNER navms ENCODING 'UTF8';
CREATE DATABASE hue OWNER hue ENCODING 'UTF8';
CREATE DATABASE oozie OWNER oozie ENCODING 'UTF8';
EOF

    # 8. Install the PostgreSQL JDBC driver
    wget -O /usr/share/java/postgresql-connector-java.jar https://jdbc.postgresql.org/download/postgresql-42.7.2.jar
    chmod 644 /usr/share/java/postgresql-connector-java.jar


    # 9. Initialize Cloudera Manager database schema with PostgreSQL
    echo "Initializing Cloudera Manager database schema..."
    /opt/cloudera/cm/schema/scm_prepare_database.sh postgresql scm scm scm_password

    # 10. Start Cloudera Manager Server
    echo "Starting Cloudera Manager Server..."
    systemctl start cloudera-scm-server

    # 11. Enable services to start on boot
    echo "Enabling Cloudera Manager services on boot..."
    systemctl enable cloudera-scm-server
    systemctl enable cloudera-scm-agent
    systemctl enable postgresql

    echo "Cloudera Manager installation completed!"
    echo "You can access the Cloudera Manager Web UI at http://<your-server-ip>:7180"
}

# Execute the function to install Cloudera Manager
install_cloudera_manager
