#!/bin/bash

# Set the path to your certificate files
certificate_path="/home/aryagami/pract/destination"

# Initialize an empty array
certificates=()

# Iterate through the files in the directory
for cert in "$certificate_path"/*.crt; do
    # Check if the file has a .crt extension
    if [ -f "$cert" ]; then
        # Add the certificate to the array
        certificates+=("$(basename $cert)")
    fi
done

# Print the array to verify
for cert in "${certificates[@]}"; do
    echo "$cert"
done
