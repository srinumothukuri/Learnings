
#!/bin/bash

csv_file="/home/aryagami/script7z/compression_status.csv"

#current_date=$(date +"%Y-%m-%d")

current_time=$(date +%H:%M:%S)

# Check if the CSV file exists, if not, create header
if [ ! -f "$csv_file" ]; then
    echo "Name,Date,Status,Size Before,Size After" > "$csv_file"
fi

# Start your 7z compression script with nohup

sudo nohup /bin/bash /home/aryagami/script7z/7zscript.sh > /home/aryagami/nohup.log 2>&1 & 

# Get the process ID (PID) of the script

pid=$!

echo $pid

# Wait for the process to finish
wait "$pid"

# Get the status
if [ $? -eq 0 ]; then
    status="success"
    before_size=$(7z l /home/aryagami/backup/compressed_file_${current_time}.7z | awk 'END{print $3/1024/1024}')
    after_size=$(7z l /home/aryagami/backup/compressed_file_${current_time}.7z | awk 'END{print $4/1024/1024}') 
else
    status="failed"
    if [ ! -f "/home/aryagami/backup/compressed_file_${current_time}.7z" ]; then
        before_size="0"
	after_size="0"
    else        
        before_size=$(7z l /home/aryagami/backup/compressed_file_${current_time}.7z | awk 'END{print $3/1024/1024}')
        after_size=$(7z l /home/aryagami/backup/compressed_file_${current_time}.7z | awk 'END{print $4/1024/1024}')
    fi   
fi


# Append data to the CSV file
echo "compressed_file_${current_time},$current_time,$status,$before_size,$after_size" >> "$csv_file"

