#!/bin/bash

mysql_user="srinivas"
mysql_password="Bulzer220"
mysql_host="localhost"
mysql_dbase="srinivas"
table_name="people"
csv_file="/home/aryagami/pract/output_data.csv"

sql_query="SELECT * FROM $table_name;"

mysql -u"$mysql_user" -p"$mysql_password" -h"$mysql_host" -D"$mysql_dbase" -e"$sql_query"|sed 's/\t/,/g'>"$csv_file"

#IFS=','

# Read and print each line from the CSV file
while read -r line; do
  echo "$line"
  sleep 2
done < "$csv_file"
