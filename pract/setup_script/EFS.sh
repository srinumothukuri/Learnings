#!/bin/bash

vpc_id=$(jq -r '.vpc_id' RDS_config.json)

region=$(jq -r '.region' RDS_config.json)

efsname=$(jq -r '.EFS_NAME' RDS_config.json)

efs_id=$(aws efs create-file-system --performance-mode generalPurpose --tags Key=Name,Value=$efsname --encrypted --region $region --query 'FileSystemId' --output text)

subnet_ids=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$vpc_id" "Name=mapPublicIpOnLaunch,Values=false" --query 'Subnets[].SubnetId' --region $region --output text)

security_id=$(jq -r '.clustersharedgroup_id' RDS_config.json)

echo "EFS creation started..."
sleep 5

for subnet_id in $subnet_ids; do
    aws efs create-mount-target --file-system-id $efs_id --subnet-id $subnet_id --security-groups $security_id --region $region
done

# Function to check if all statuses are "available"
check_statuses() {
    status_variable=$(aws efs describe-mount-targets --file-system-id $efs_id --region $region --query 'MountTargets[].LifeCycleState' --output text)

    IFS=$'\t' read -r -a status_array <<< "$status_variable"
    for status in "${status_array[@]}"
    do
        if [ "$status" != "available" ]; then
            return 1
        fi
    done
    return 0
}

# Continuously check statuses until all are "available"
while true
do
    check_statuses
    if [ $? -eq 0 ]; then
        echo "All mount targets are in an available state. Continuing the script..."

        filesystem_id=$(aws efs describe-file-systems --query "FileSystems[0].FileSystemId")

        ip_address=$(aws efs describe-mount-targets --file-system-id $filesystem_id --query 'MountTargets[0].IpAddress')

        sed -i "s/REPLACE_WITH_ID/$filesystem_id/" ~/pract/setup_script/efs-yamls/pv.yml
        sed -i "s/REPLACE_WITH_EFS_IP/$ip_address/" ~/pract/setup_script/efs-yamls/nfsdeployment.yml
        echo "Creating necessary dependencies for EFS..."

        namespace=$(jq -r '.namespace' RDS_config.json)

        kubectl apply -f ~/pract/setup_script/efs-yamls -n $namespace

        sec=30
        while [ $sec -ge 1 ]; do
            sleep 1
            : $((sec--))
            echo -ne "\rCountdown: $sec seconds "
        done

        sed -i "s/$filesystem_id/REPLACE_WITH_ID/" ~/pract/setup_script/efs-yamls/pv.yml

        sed -i "s/$ip_address/REPLACE_WITH_EFS_IP/" ~/pract/setup_script/efs-yamls/nfsdeployment.yml


        echo " "

        echo "Creating pods..."

        kubectl apply -f ~/pract/setup_script/pods -n $namespace

        echo "Finishing..."
        sleep 60
        echo " "
        echo "Done"
        break
    else
        echo "Not all mount targets are in an available state. Waiting..."
        sleep 10  # Adjust the sleep duration as needed
    fi
done

echo "Continuing to next stage..."
echo " "
source  /home/aryagami/pract/setup_script/RDS.sh
