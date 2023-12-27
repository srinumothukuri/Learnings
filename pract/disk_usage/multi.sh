
#!/bin/bash

SUBJECT="Lyca Servers Disk-usage report"

servers=("172.31.8.53" "172.31.8.8" "172.31.8.17" "172.31.8.18")

html_content="<html><head><style>table {border-collapse: collapse; width: 100%;} th, td {border: 1px solid #dddddd; text-align: left; padding: 8px;} th {background-color: #f2f2f2;}</style></head><body><h2>Lyca Servers Disk-usage report</h2>"

for server in "${servers[@]}"; do
    # Get server IP address and hostname, store in variables
    server_ip=$(ssh -i ~/Downloads/keypair ubuntu@"$server" hostname -I | awk '{print $1}')
    host_name=$(ssh -i ~/Downloads/keypair ubuntu@"$server" hostname)

    # Run the 'df -h' command via SSH, excluding the first column using 'tail', and store the output in a variable
    df_output=$(ssh -i ~/Downloads/keypair ubuntu@"$server" df -h | tail -n +2)

    # Use awk to format the output into a table with added columns for server IP and hostname
    formatted_output=$(echo "$df_output" | awk -v ip="$server_ip" -v host="$host_name" '{printf "%-15s%-18s%-15s%-10s%-12s%-10s%s\n", ip, host, $2, $3, $4, $5, $6}')
   #formatted_output=$(echo "$df_output" | awk  '{printf "%-15s%-18s%-15s%-10s%-12s%-10s%s\n",$1, $2, $3, $4, $5, $6}')

    html_content+="<h3>$server</h3><table><tr><th>Server IP</th><th>hostname</th><th>Size</th><th>Used</th><th>Available</th><th>Usage</th><th>Path</th></tr>"

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

    html_content+="</table>"
done

# Close the HTML content
html_content+="</body></html>"

echo "$html_content"

#python3 /home/aryagami/disk_usage/alert.py "$html_content" "$SUBJECT"
