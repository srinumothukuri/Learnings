#!/bin/bash

# Define the file path and name
f1="/home/aryagami/pract/setup_script/EFS.sh"
f2="/home/aryagami/pract/setup_script/RDS.sh"
f3="/home/aryagami/pract/setup_script/mysql.sh"
f4="/home/aryagami/pract/setup_script/allpods.sh"
f5="/home/aryagami/pract/setup_script/RDS_config.json"
f6="/home/aryagami/pract/setup_script/allyamls"
f7="/home/aryagami/pract/setup_script/config-server"
f8="/home/aryagami/pract/setup_script/efs-yamls"
f9="/home/aryagami/pract/setup_script/connection"
f10="/home/aryagami/pract/setup_script/pods"
f11="/home/aryagami/pract/setup_script/mysql-client.yml"
f12="/home/aryagami/properties"

if [ -e "$f1" ]; then
    echo "EFS file exists"
else
    echo "EFS file does not exist. Exiting."
    exit 1
fi

if [ -e "$f2" ]; then
    echo "RDS file exists"

else
    echo "RDS file does not exist. Exiting."
    exit 1
fi

if [ -e "$f3" ]; then
    echo "mysql file exists"

else
    echo "mysql file does not exist. Exiting."
    exit 1
fi

if [ -e "$f4" ]; then
    echo "allpods file exists"

else
    echo "allpods file does not exist. Exiting."
    exit 1
fi


if [ -e "$f5" ]; then
    echo "config-json file exists"

else
    echo "config-json file does not exist. Exiting."
    exit 1
fi

if [ -e "$f6" ]; then
    echo "allyamls directory exists"

else
    echo "allyamls directory does not exist. Exiting."
    exit 1
fi

if [ -e "$f7" ]; then
    echo "config-server directory exists"

else
    echo "config-server directory does not exist. Exiting."
    exit 1
fi

if [ -e "$f8" ]; then
    echo "efs-yamls directory exists"

else
    echo "efs-yamls directory does not exist. Exiting."
    exit 1
fi

if [ -e "$f9" ]; then
    echo "connection directory exists"

else
    echo "connection directory does not exist. Exiting."
    exit 1
fi
if [ -e "$f10" ]; then
    echo "pods directory exists"

else
    echo "pods directory does not exist. Exiting."
    exit 1
fi
if [ -e "$f11" ]; then
    echo "mysql-client pod file exists"

else
    echo "mysql-client pod file does not exist. Exiting."
    exit 1
fi
if [ -e "$f12" ]; then
    echo "properties directory exists"

else
    echo "properties directory does not exist. Exiting."
    exit 1
fi

echo " "
echo " "

source /home/aryagami/pract/setup_script/EFS.sh
