#!/bin/bash

namespace=$(jq -r '.namespace' RDS_config.json)

echo "Setting up config-server deployment..."

kubectl apply -f ~/pract/setup_script/config-server -n $namespace

pod=$(kubectl get po -n $namespace | grep "config" |awk '{print $1}')

echo "Waiting for pod to enter running state..."

while [[ "$(kubectl get pod $pod -n $namespace -o jsonpath='{.status.phase}')" != "Running" ]]; do 
    sleep 5
done

echo "Pod $pod is now in Running state."
echo " "

echo "Waiting for 30 seconds..."
echo " "

sec=30
while [ $sec -ge 1 ]; do
    sleep 1 
    : $((sec--))
    echo -ne "\rCountdown: $sec seconds "
done

echo " "

echo "Copying necessary properties..."

kubectl cp /home/aryagami/properties/. $pod:/opt/config_server -n $namespace

echo " "

echo "Properties copied"
echo " "
count=30
while [ $count -ge 1 ]; do
    sleep 1 
    : $((count--))
    echo -ne "\rCountdown: $count seconds "
done

echo " "
echo "Setting up all pods..."
kubectl apply -f ~/pract/setup_script/allyamls -n $namespace

echo " "
echo "Pods are setting up...can take some time"
sleep 90

echo "Done"

