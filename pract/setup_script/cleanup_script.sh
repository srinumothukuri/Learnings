#!/bin/bash

ns=$(jq -r '.namespace' RDS_config.json)
region=$(jq -r '.region' RDS_config.json)
DBName=$(jq -r '.DBName' RDS_config.json)
efsname=$(jq -r '.EFS_NAME' RDS_config.json)

efs_id=$(aws efs describe-file-systems --region $region --output json | jq -r '.FileSystems[] | select(.Name == "$efsname").FileSystemId')


kubectl delete -f ~/pract/setup_script/allyamls -n $ns
sleep 30
kubectl delete -f ~/pract/setup_script/config-server -n $ns
sleep 15
kubectl delete -f ~/pract/setup_script/pods -n $ns
sleep  15
kubectl delete -f ~/pract/setup_script/efs-yamls -n $ns
sleep 15
kubectl delete -f ~/pract/setup_script/connection -n $ns
sleep 10
kubectl delete -f ~/pract/setup_script/mysql-client.yml -n $ns

#aws rds delete-db-instance --db-instance-identifier $DBName --skip-final-snapshot --region $region

# Step 1: Fetch Mount Targets
mount_targets=$(aws efs describe-mount-targets --file-system-id $efs_id --query 'MountTargets[].MountTargetId' --output text)

# Step 2: Delete Mount Targets
for mt in $mount_targets
do
    aws efs delete-mount-target --mount-target-id $mt
    sleep 20
    echo "Deleted mount target: $mt"
done
sleep 5

echo "Deleting File system..."
aws efs delete-file-system --file-system-id $efs_id

sleep 5

aws rds delete-db-instance --db-instance-identifier $DBName --skip-final-snapshot --region $region


