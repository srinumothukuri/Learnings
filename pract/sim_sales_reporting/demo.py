
from datetime import datetime, timedelta
import mysql.connector
import csv
import subprocess

def execute_query(query):
    connection = mysql.connector.connect(
        host="billingrepo",
        user="billing",
        password="access",
        database="billing"
    )
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()
    return result



yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
d={}
e={}
count=1


for hour in range(11,12):
    current_hour = str(hour).zfill(2)
    # Handle transition to the next day
    if current_hour == '24':
        next_date = (datetime.strptime(yesterday, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
        current_hour = '00'
    else:
        next_date = yesterday
    print (next_date)
    print(current_hour)
    # Get reseller_code values
    print(f"SELECT reseller_code FROM subscription WHERE created_date >= '{yesterday} 00:00:00' AND created_date < '{next_date} {current_hour}:00:00' GROUP BY reseller_code;")
    reseller_codes = execute_query(f"SELECT reseller_code FROM subscription WHERE created_date >= '{yesterday} 00:00:00' AND created_date < '{next_date} {current_hour}:00:00' GROUP BY reseller_code;")
 #   print(reseller_codes)
    if reseller_codes:
        for reseller_code in reseller_codes:
            reseller_code = reseller_code[0]
           # print(reseller_code)
            sim_sales = execute_query(f"SELECT count(*) FROM subscription WHERE reseller_code = '{reseller_code}' AND created_date >= '{yesterday} 00:00:00' AND created_date < '{next_date} {current_hour}:00:00';")[0][0]
            user_info = execute_query(f"SELECT user_id, aggregator_id FROM reseller_management WHERE reseller_id = '{reseller_code}';")
            #print(user_info)
            if user_info:
                user_id, aggregator_id = user_info[0]
                reseller_name = execute_query(f"SELECT user_name FROM user WHERE user_id = '{user_id}';")[0][0]
                distributor_info = execute_query(f"SELECT user_id, aggregator_id FROM reseller_management WHERE reseller_id = '{aggregator_id}';")
                if distributor_info:
                    distributor_id, distributor_aggregator_id = distributor_info[0]
                    distributor_name = execute_query(f"SELECT user_name FROM user WHERE user_id = '{distributor_id}';")[0][0]
                    aggregator_info = execute_query(f"SELECT user_id, aggregator_id FROM reseller_management WHERE reseller_id = '{distributor_aggregator_id}';")
                    if aggregator_info:
                        aggregator_id = aggregator_info[0][0]
                        aggregator_name = execute_query(f"SELECT user_name FROM user WHERE user_id = '{aggregator_id}';")[0][0]

                        if aggregator_name in d:
                            d[aggregator_name]=d[aggregator_name]+sim_sales
                            e[aggregator_name]+=1
                        else:
                            d[aggregator_name]=sim_sales
                            e[aggregator_name]=count
    print(d)
    print(e)

