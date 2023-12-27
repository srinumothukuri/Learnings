#!/bin/bash

user="srinivas"
password="Bulzer220"
host="localhost"
csvfile="/home/aryagami/pract/data.csv"
tablename="people"
dbase="srinivas"



csv_header=$(head -n 1 "$csvfile")


columns=$(echo "$csv_header"|awk 'BEGIN {FS=OFS=","} NR==1 {
suffix[1]=" INT(10)"
suffix[2]=" VARCHAR(255)"
suffix[3]=" VARCHAR(255)"
suffix[4]=" INT(100)"

for (i=1; i<=NF; i++) $i = $i suffix[i]}
 1')


sqlcreate="CREATE TABLE $tablename ($columns);"

loaddata="LOAD DATA LOCAL INFILE '$csvfile' INTO TABLE $tablename FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 LINES;"

sudo mysql -u"$user" -p"$password" -h "$host" -D "$dbase" -e "$sqlcreate"


sudo mysql -u"$user" -p"$password" -h "$host" -D "$dbase" -e "$loaddata"
echo "Data loaded to SQL Table successfully"
