#!/bin/bash

# Define the source and destination directories
#source_dir="/opt/cdr_vol/processed_voip_cdrs"
#destination_dir="/opt/cdr_vol/voip_cdr"

source_dir="/home/aryagami/source"
destination_dir="/home/aryagami/pract/destination"



# Define the start and end dates (in YYYY-MM-DD format)
start_date="2023-10-01"             # Start date is inclusive
end_date="2023-10-07"               # End date is exclusive


# To copy files and directories

find "$source_dir" -mindepth 1 -type f -newermt "$start_date" ! -newermt "$end_date" -exec bash -c 'cp -r "$0" "$1"' {} "$destination_dir" \;

#find "$source_dir" -maxdepth 1 -type f -newermt "$start_date" ! -newermt "$end_date" -exec cp -t "$destination_dir" {} +

# To move files and directories

#find "$source_dir" -mindepth 1 -type d -newermt "$start_date" ! -newermt "$end_date" -exec mv -t "$destination_dir" {} +

#find "$source_dir" -maxdepth 1 -type f -newermt "$start_date" ! -newermt "$end_date" -exec mv -t "$destination_dir" {} +


