#!/bin/bash

# Read the values from the config file

DBName=$(jq -r '.DBName' RDS_config.json)
MasterPassword=$(jq -r '.MasterPassword' RDS_config.json)
AvailabilityZone=$(jq -r '.AvailabilityZone' RDS_config.json)
SecurityGroups=$(jq -r '.SecurityGroups | join(" ")' RDS_config.json)
SubnetGroupName=$(jq -r '.SubnetGroupName' RDS_config.json)

aws rds create-db-instance \
    --db-instance-identifier "$DBName" \
    --allocated-storage 20 \
    --db-instance-class db.t3.micro \
    --engine mysql \
    --master-username root \
    --master-user-password "$MasterPassword" \
    --db-subnet-group-name "$SubnetGroupName" \
    --availability-zone "$AvailabilityZone" \
    --storage-type gp2 \
    --auto-minor-version-upgrade \
    --vpc-security-group-ids $SecurityGroups \
    --tags Key=Name,Value="$DBName"


countdown=180
while [ $countdown -ge 0 ]; do
    status=$(aws rds describe-db-instances --db-instance-identifier $DBName --query 'DBInstances[0].DBInstanceStatus' --output text)
    if [ "$status" = "available" ]; then
        break
    fi
    echo "RDS instance status: $status"
    sleep 10
    : $((countdown--))
done

# Check if RDS instance is available
if [ "$status" = "available" ]; then
    echo "RDS instance is available. Continuing to next stage..."
    source /home/aryagami/pract/setup_script/mysql.sh
else
    echo "Timed out waiting for RDS instance to become available."
fi
