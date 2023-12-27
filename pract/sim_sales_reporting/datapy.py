from datetime import datetime, timedelta
import mysql.connector

# Function to execute MySQL queries
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

# Get previous and current dates
previous_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
runtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Create a CSV file and write headers
with open(f"/home/ubuntu/summary/data_details_{previous_date}.csv", "w") as file:
    file.write("\"Date\",\"Run_time\",\"Retailer_Name\",\"Distributor_name\",\"Aggregator_name\",\"Sim_sales\",\"Hour\"\n")

# Get yesterday's date
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

for hour in range(9,10):
    current_hour = str(hour).zfill(2)
    next_hour = str((hour + 1) % 24).zfill(2)
    
    # Handle transition to the next day
    if next_hour == '00':
        next_date = (datetime.strptime(yesterday, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
    else:
        next_date = yesterday

    # Get reseller_code values
    #reseller_codes = execute_query(f"SELECT reseller_code FROM subscription WHERE created_date > '{yesterday} {current_hour}:00:00' AND created_date < '{next_date} {next_hour}:00:00' GROUP BY reseller_code;")
    reseller_codes = execute_query(f"SELECT reseller_code FROM subscription WHERE created_date > '{yesterday} 00:00:00' AND created_date < '{next_date} {current_hour}:00:00' GROUP BY reseller_code;")
   # print(reseller_codes)
    if reseller_codes:
        for reseller_code in reseller_codes:
            reseller_code = reseller_code[0]
           # print(reseller_code)
            sim_sales = execute_query(f"SELECT count(*) FROM subscription WHERE reseller_code = '{reseller_code}' AND created_date > '{yesterday} 00:00:00' AND created_date < '{next_date} {current_hour}:00:00';")[0][0]
            hour_sales = execute_query(f"SELECT hour(created_date) FROM subscription WHERE reseller_code = '{reseller_code}' AND created_date > '{yesterday} 00:00:00' AND created_date < '{next_date} {current_hour}:00:00' GROUP BY hour(created_date);")[0][0]
            user_info = execute_query(f"SELECT user_id, aggregator_id FROM reseller_management WHERE reseller_id = '{reseller_code}';")
            print(user_info)
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

                        with open(f"/home/ubuntu/summary/data_details_{previous_date}.csv", "a") as file:
                            file.write(f"\"{previous_date}\",\"{runtime}\",\"{reseller_name}\",\"{distributor_name}\",\"{aggregator_name}\",\"{sim_sales}\",\"{hour_sales}\"\n")
    else:
        print("No reseller codes found. Skipping loop.")

print("\nData details done...")

