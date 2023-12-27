



#!/bin/bash

previous_date=$(date -d "yesterday" +'%Y-%m-%d')
runtime=$(date +'%Y-%m-%d %H:%M:%S')
echo "\"Date\",\"Run_time\",\"Retailer_Name\",\"Distributor_name\",\"Aggregator_name\",\"Sim_sales\",\"Hour\"" > /home/ubuntu/summary/data_details_$previous_date.csv

current_date=$(date +'%Y-%m-%d')
yesterday=$(date -d "yesterday" +'%Y-%m-%d')

for ((hour=0; hour<24; hour++)); do
  current_hour=$(printf "%02d" $hour)
  next_hour=$((hour + 1))
  next_hour=$(printf "%02d" $next_hour)

  # Handle transition to the next day
  if [ $next_hour -eq 24 ]; then
        next_hour="00"
        next_date=$(date -d "$yesterday +1 day" +%Y-%m-%d)
  else
        next_date=$yesterday
  fi

  # Get reseller_code values and store them in a temporary variable
  reseller_codes=$(mysql -h billingrepo -u billing -paccess billing -e "SELECT reseller_code FROM subscription WHERE created_date > '$yesterday $current_hour:00:00'  AND created_date < '$next_date $next_hour:00:00' GROUP BY reseller_code;" -N)
  echo "$current_hour"
  echo "$next_hour"
  echo "$next_date"
if [ -n "$reseller_codes" ]; then

  # Loop through the reseller codes
  while read -r reseller_code; do
      echo "$reseller_code"
      sim_sales=$(mysql -h billingrepo -u billing -paccess billing -e "SELECT count(*) FROM subscription WHERE reseller_code = '$reseller_code' and created_date > '$yesterday $current_hour:00:00' AND created_date < '$next_date $next_hour:00:00';" -N)
      hour_sales=$(mysql -h billingrepo -u billing -paccess billing -e "SELECT hour(created_date) FROM subscription WHERE reseller_code = '$reseller_code' and created_date > '$yesterday $current_hour:00:00' AND created_date < '$next_date $next_hour:00:00' GROUP BY hour(created_date);" -N)

      # Retrieve user_id and aggregator_id based on the reseller_code
      reseller_info=$(mysql -h billingrepo -u billing -paccess billing -e "SELECT user_id, aggregator_id FROM reseller_management WHERE reseller_id = '$reseller_code';" -N)

      # Extract user_id from user_aggregator_info
      user_id=$(echo "$reseller_info" | cut -d$'\t' -f1)

      # Fetch user_name based on user_id
      reseller_name=$(mysql -h billingrepo -u billing -paccess billing -e "SELECT user_name FROM user WHERE user_id = '$user_id';" -N)

      # Extract aggregator_id from user_aggregator_info
      re_aggregator_id=$(echo "$reseller_info" | cut -d$'\t' -f2)

      distributor_info=$(mysql -h billingrepo -u billing -paccess billing -e "SELECT user_id, aggregator_id FROM reseller_management WHERE reseller_id = '$re_aggregator_id';" -N)

      dis_id=$(echo "$distributor_info" | cut -d$'\t' -f1)

      dis_name=$(mysql -h billingrepo -u billing -paccess billing -e "SELECT user_name FROM user WHERE user_id = '$dis_id';" -N)

      dis_aggregator_id=$(echo "$distributor_info" | cut -d$'\t' -f2)

      aggregator_info=$(mysql -h billingrepo -u billing -paccess billing -e "SELECT user_id, aggregator_id FROM reseller_management WHERE reseller_id = '$dis_aggregator_id';" -N)

      agg_id=$(echo "$aggregator_info" | cut -d$'\t' -f1)


      agg_name=$(mysql -h billingrepo -u billing -paccess billing -e "SELECT user_name FROM user WHERE user_id = '$agg_id';" -N)

      agg_aggregator_id=$(echo "$aggregator_info" | cut -d$'\t' -f2)

      # Append the retrieved information into the respective CSV files
      echo "\"$previous_date\",\"$runtime\",\"$reseller_name\",\"$dis_name\",\"$agg_name\",\"$sim_sales\",\"$hour_sales\"" >> /home/ubuntu/summary/data_details_$previous_date.csv
  done <<< "$reseller_codes"
  else
    echo "No reseller codes found. Skipping loop."
 fi 

done

echo " "
echo "Data details done..."

sudo python3 /home/ubuntu/sim_sales_reporting/mail.py
