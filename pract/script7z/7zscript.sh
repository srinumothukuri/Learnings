

#!/bin/bash

# File to compress
file_to_compress="/home/aryagami/srinivas-xtrabackup"  # Replace this with the path to your file

# Output directory
output_directory="/home/aryagami/backup"  # Replace this with the desired output directory

# Get the current date
#current_date=$(date +"%Y-%m-%d")

current_time=$(date +%H:%M:%S)


# Compress the file using 7z
7z a "${output_directory}/compressed_file_${current_time}.7z" "$file_to_compress"

#7z a -m9=lzma2 "${output_directory}/compressed_file_${current_date}.7z" "$file_to_compress"


# This command will remove files older than 4 days.
#find "${output_directory}" -type f -name "compressed_file_*" -mtime +4 -exec rm {} \;
