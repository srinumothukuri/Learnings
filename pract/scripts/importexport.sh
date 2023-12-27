#!/bin/bash
read -p"enter csv file name: " file
csv_file="/home/aryagami/pract/$file$(date +'%F %T').csv"
sudo mysql -usrinivas -pBulzer220 -Dsrinivas <<EOF
CREATE TABLE mytable (
  sno INTEGER,
  name TEXT,
  current_date_time TEXT
);
EOF

insertvalues() {
  current_date_time=$(date +"%Y-%m-%d %H:%M:%S")
  sudo mysql -usrinivas -pBulzer220 -Dsrinivas -e  "INSERT INTO mytable (sno, name, current_date_time) VALUES ($1, 'Name$1', '$current_date_time');"
}

exporttocsv() {
  sudo mysql -usrinivas -pBulzer220 -Dsrinivas -e "SELECT * FROM mytable;" | sed 's/\t/,/g'>"$csv_file"
  echo "CSV file created: $csv_file"
  cat "$csv_file"
}
for ((i=1; i<=10; i++)); do
  insertvalues $i
  sleep 1

  if ((i % 3 == 0)); then
    exporttocsv
    sleep 3
  fi
done
exporttocsv
