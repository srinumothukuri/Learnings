#!/bin/bash

namespace=$(jq -r '.namespace' RDS_config.json)
DBName=$(jq -r '.DBName' RDS_config.json)
rds_endpoint=$(aws rds describe-db-instances --db-instance-identifier $DBName --query 'DBInstances[0].Endpoint.Address' --output text)
masterpassword=$(jq -r '.MasterPassword' RDS_config.json)

echo "Creating mysql pod"

kubectl apply -f ~/pract/setup_script/mysql-client.yml -n $namespace
pod_name="mysql-client-pod"


echo "Waiting for pod to enter running state..."

while [[ "$(kubectl get pod $pod_name -n $namespace -o jsonpath='{.status.phase}')" != "Running" ]]; do 
    sleep 5
done

echo "Pod $pod_name is now in Running state."

# Read database names from the JSON config file
database_names=$(jq -r '.databases[]' RDS_config.json)

echo "Creating Databases..."

sleep 10

# Iterate through each database name and create the database
for dbname in $database_names; do
    kubectl exec -n $namespace  $pod_name -- mysql -h $rds_endpoint -u root -p$masterpassword -e "CREATE DATABASE IF NOT EXISTS $dbname ;"
    echo " Database $dbname created"
    sleep 5
done

# Read the JSON file and extract the username and password
username=$(jq -r '.mysql_username' RDS_config.json)
password=$(jq -r '.mysql_password' RDS_config.json)

echo "Creating user $username ..."

# Create the user and grant privileges
kubectl exec -n $namespace $pod_name -- mysql -h $rds_endpoint -u root -p$masterpassword -e "CREATE USER '$username'@'%' IDENTIFIED BY '$password';"

# Grant privileges for all databases
kubectl exec -n $namespace $pod_name -- mysql -h $rds_endpoint -u root -p$masterpassword -e "GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP,RELOAD,ALTER,REFERENCES ON *.* TO 'billing'@'%';"

kubectl exec -n $namespace $pod_name -- mysql -h $rds_endpoint -u root -p$masterpassword -e "FLUSH PRIVILEGES;"

echo "User $username granted privileges for all databases"

echo "Deploying repo's for RDS-mysql..."


#rds_endpoint=$(aws rds describe-db-instances --db-instance-identifier dummy --query 'DBInstances[0].Endpoint.Address' --output text)

# Replace the placeholder in the Service YAML
sed -i "s/REPLACE_WITH_ENDPOINT/$rds_endpoint/g" ~/pract/setup_script/connection/updated-services.yml

# Apply the modified YAML to your cluster
kubectl apply -f ~/pract/setup_script/connection/updated-services.yml -n $namespace

# Restore the original placeholder for future runs
sed -i "s/$rds_endpoint/REPLACE_WITH_ENDPOINT/g" ~/pract/setup_script/connection/updated-services.yml

sleep 10

echo "Done"

echo "Continuing to next stage..."

source ~/pract/setup_script/allpods.sh
