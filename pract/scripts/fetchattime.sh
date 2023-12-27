#!/bin/bash

read -p"Enter file name: " file
csv_file="/home/aryagami/pract/$file$(date +'%F %T').csv"

start="2023-07-31_18:58:40"
end="2023-07-31_18:59:00"

create_table(){

	sudo mysql -usrinivas -pBulzer220 -hlocalhost -Dsrinivas <<EOF
	create table if not exists datafetch(
	id INT AUTO_INCREMENT PRIMARY KEY,
	data VARCHAR(255),
	timestamp DATETIME
);
EOF
}

insert_data(){

	time_stamp=$(date +"%F_%T")
	value=$1
	sudo mysql -usrinivas -pBulzer220 -hlocalhost -Dsrinivas -e "insert into datafetch (data,timestamp) values ('data $value','$time_stamp');"
}


print_data(){

	sudo mysql -usrinivas -pBulzer220 -hlocalhost -Dsrinivas -e "select * from datafetch where timestamp between '$start' and '$end';"|sed 's/\t/,/g'>"$csv_file"
	cat "$csv_file"

}

create_table
n=1
while [[ "$(date +'%F_%T')" < $end ]]; do

	insert_data $n
	sleep 2
	n=$((n+1))
done

print_data
