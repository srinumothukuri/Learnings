#!/bin/bash

# Set the path to your certificate file

certificate_path="/home/aryagami/pract/destination"

# Initialize an empty array
certificates=()

# Iterate through the files in the directory
for cert in "$certificate_path"/*.crt; do
    # Check if the file has a .crt extension
    if [ -f "$cert" ]; then
        # Add the certificate to the array
        certificates+=("$cert")
    fi
done

for cert in "${certificates[@]}"; do
    echo "$cert"
done


current_date=$(date +%s)


for cert in "${certificates[@]}"
do
     expiry_date=$(date -d "$(openssl x509 -noout -enddate -in "$cert" | cut -d= -f 2)" +%s)
     notification_date=$(date -d "@$((current_date + 10 * 24 * 60 * 60))" +%s)
     expiration_date=$(openssl x509 -noout -enddate -in "$cert" | awk -F= '{print $2}')
     formatted_date=$(date -d "$expiration_date" '+%Y-%m-%d %H:%M:%S')

#     echo $notification_date
#     echo $expiry_date
     if [ "$expiry_date" -le "$notification_date" ]; then
#         echo $notification_date
#         echo $expiry_date
         python3 /home/aryagami/alert_certs/send_email.py "$(basename $cert)" "$formatted_date"
         echo "Notification sent!"
     else
         echo "Certificate is not expiring in the next 10 days."
     fi
done
