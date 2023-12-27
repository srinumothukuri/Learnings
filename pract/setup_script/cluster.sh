#!/bin/bash

# Prompt the user for the cluster name
echo "Enter a vpc_id:"
read vpc_id
echo "Enter a name for the cluster:"
read cluster_name

# Run the AWS CLI command and store the output in a variable
subnet_ids=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$vpc_id" "Name=mapPublicIpOnLaunch,Values=false" --query 'Subnets[].SubnetId' --output text)

# Convert the space-separated string of IDs into an array
IFS=$'\t' read -r -a subnet_array <<< "$subnet_ids"

# Access the IDs using array indices
# Check number of subnets available and change as per required

subnet_1=${subnet_array[0]}
subnet_2=${subnet_array[1]}
subnet_3=${subnet_array[2]}

# Create cluster using user-provided name
eksctl create cluster --name "$cluster_name" --region ap-south-1 --version 1.26 --vpc-private-subnets $subnet_1,$subnet_2,$subnet_3 --without-nodegroup --fargate
