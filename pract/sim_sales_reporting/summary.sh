


#!/bin/bash
current_date=$(date +'%Y-%m-%d')
previous_date=$(date -d "yesterday" +'%Y-%m-%d')
query="SELECT
    u.user_name,
    SUM(CASE WHEN HOUR(s.created_date) = 0 THEN 1 ELSE 0 END) AS 'Hour_00',
    SUM(CASE WHEN HOUR(s.created_date) = 1 THEN 1 ELSE 0 END) AS 'Hour_01',
    SUM(CASE WHEN HOUR(s.created_date) = 2 THEN 1 ELSE 0 END) AS 'Hour_02',
    SUM(CASE WHEN HOUR(s.created_date) = 3 THEN 1 ELSE 0 END) AS 'Hour_03',
    SUM(CASE WHEN HOUR(s.created_date) = 4 THEN 1 ELSE 0 END) AS 'Hour_04',
    SUM(CASE WHEN HOUR(s.created_date) = 5 THEN 1 ELSE 0 END) AS 'Hour_05',
    SUM(CASE WHEN HOUR(s.created_date) = 6 THEN 1 ELSE 0 END) AS 'Hour_06',
    SUM(CASE WHEN HOUR(s.created_date) = 7 THEN 1 ELSE 0 END) AS 'Hour_07',
    SUM(CASE WHEN HOUR(s.created_date) = 8 THEN 1 ELSE 0 END) AS 'Hour_08',
    SUM(CASE WHEN HOUR(s.created_date) = 9 THEN 1 ELSE 0 END) AS 'Hour_09',
    SUM(CASE WHEN HOUR(s.created_date) = 10 THEN 1 ELSE 0 END) AS 'Hour_10',
    SUM(CASE WHEN HOUR(s.created_date) = 11 THEN 1 ELSE 0 END) AS 'Hour_11',
    SUM(CASE WHEN HOUR(s.created_date) = 12 THEN 1 ELSE 0 END) AS 'Hour_12',
    SUM(CASE WHEN HOUR(s.created_date) = 13 THEN 1 ELSE 0 END) AS 'Hour_13',
    SUM(CASE WHEN HOUR(s.created_date) = 14 THEN 1 ELSE 0 END) AS 'Hour_14',
    SUM(CASE WHEN HOUR(s.created_date) = 15 THEN 1 ELSE 0 END) AS 'Hour_15',
    SUM(CASE WHEN HOUR(s.created_date) = 16 THEN 1 ELSE 0 END) AS 'Hour_16',
    SUM(CASE WHEN HOUR(s.created_date) = 17 THEN 1 ELSE 0 END) AS 'Hour_17',
    SUM(CASE WHEN HOUR(s.created_date) = 18 THEN 1 ELSE 0 END) AS 'Hour_18',
    SUM(CASE WHEN HOUR(s.created_date) = 19 THEN 1 ELSE 0 END) AS 'Hour_19',
    SUM(CASE WHEN HOUR(s.created_date) = 20 THEN 1 ELSE 0 END) AS 'Hour_20',
    SUM(CASE WHEN HOUR(s.created_date) = 21 THEN 1 ELSE 0 END) AS 'Hour_21',
    SUM(CASE WHEN HOUR(s.created_date) = 22 THEN 1 ELSE 0 END) AS 'Hour_22',
    SUM(CASE WHEN HOUR(s.created_date) = 23 THEN 1 ELSE 0 END) AS 'Hour_23'
FROM
    subscription s
JOIN
    reseller_management r ON s.reseller_code = r.reseller_id
JOIN
    user u ON r.user_id = u.user_id
WHERE
    s.created_date >= '$previous_date 00:00:00' and  s.created_date < '$current_date 00:00:00'
GROUP BY
    u.user_name
ORDER BY
    u.user_name;"



mysql -hbillingrepo -ubilling -paccess billing -e "$query" -B | sed "s/'/\'/;s/\t/\",\"/g;s/^/\"/;s/$/\"/;s/\n//g" > /home/ubuntu/summary/summary_$previous_date.csv

#echo "$current_date"

#echo "$previous_date"

echo "Summary file done ..."

sudo /bin/bash /home/ubuntu/sim_sales_reporting/data_details.sh

