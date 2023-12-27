
#!/bin/bash

# Get server IP address and hostname, store in variables
server_ip=$(hostname -I | awk '{print $1}')
host_name=$(hostname)
SUBJECT="Disk usage"

# Run the 'df -h' command, excluding the first column using 'tail' and store the output in a variable
df_output=$(df -h | tail -n +2)


formatted_output=$(echo "$df_output" | awk -v ip="$server_ip" -v host="$host_name" '{printf "%-15s%-18s%-15s%-10s%-12s%-10s%s\n", ip, host, $2, $3, $4, $5, $6}')

html_content="<html><head><style>table {border-collapse: collapse; width: 100%;} th, td {border: 1px solid #dddddd; text-align: left; padding: 8px;} th {background-color: #f2f2f2;}</style></head><body><h2>Disk Usage Report</h2><table><tr><th>Server IP</th><th>Hostname</th><th>Size</th><th>Used</th><th>Available</th><th>Usage</th><th>Path</th></tr>"


while IFS= read -r line; do
    html_content+="<tr>"
    usage=$(echo "$line" | awk '{print $6}' | tr -d '%')  # Extract 'Usage' value (assuming it's in the 6th column)
    highlight_row=false

    # Check if the usage is greater than or equal to 80% to determine row highlighting
    if [[ $usage -ge 80 ]]; then
        highlight_row=true
    fi

    for item in $line; do
        if $highlight_row; then
            html_content+="<td style='background-color:red'>$item</td>"  # Highlight the entire row in red
        else
            html_content+="<td>$item</td>"
        fi
    done
    html_content+="</tr>"
done <<< "$formatted_output"


#Close the HTML content
html_content+="</table></body></html>"

#echo "$html_content"

python /home/ubuntu/disk_usage/alert.py "$html_content" "$SUBJECT"
