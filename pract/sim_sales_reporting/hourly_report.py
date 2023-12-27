from datetime import datetime, timedelta
import mysql.connector
import csv
import subprocess
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

def name_exists(name, column_index, data):
    for row in data:
        if row[column_index] == name:
            return True
    return False

def add_values_to_csv(names_values_dict, column_index, data):
    header = data[0]
    print(header)
    if current_hour == '00':
      header.append('Full day')  
    else:
      header.append(current_hour + ':00')  # Replace 'New Column Header' with your header name
    if current_hour != '09':
       for row in data[1:]:
           print(row)
           name = row[column_index]
           if name in names_values_dict:
               value = names_values_dict[name]
#               row.append(value)
               if len(row)==1:
                  for i in range(num_columns-1):
                      row.append(0)
                  row.append(value)
               else:
                   row.append(value)
           else:
               row.append('')  # If no value exists for the name, add an empty string or any default value
    else:
       for row in data[1:]:
           print(row)
           name = row[column_index]
           if name in names_values_dict:
               value = names_values_dict[name]
               row.append(value)        
           else:
               row.append('') 

def files(filepath,dictionary):
    if current_hour == '09':
        existing_file = filepath
        input_data = [['Aggregator_name']]
        with open(existing_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(input_data)

    existing_file = filepath

    names_values = dictionary
    with open(existing_file, mode='r') as file:
        csv_reader = csv.reader(file)
        data = list(csv_reader)
        print(data)
    global num_columns
    num_columns = len(data[0]) if data else 0

    print(f"The number of columns in the CSV file is: {num_columns}")
    # Assuming the names are in the first column (column index 0)
    column_index_to_check = 0

    # Check and add new names if they don't exist
    for name, value in names_values.items():
        if not name_exists(name, column_index_to_check, data):
            data.append([name])  # Assuming the new name goes in a new row

    # Add values to the corresponding names in the CSV
    add_values_to_csv(names_values, column_index_to_check, data)

    # Write back to the CSV file
    with open(existing_file, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(data)


today = datetime.now().strftime('%Y-%m-%d')
current_time = datetime.now()
current = current_time.hour
#current = 0
if current == 0:
    current=24
#today = '2023-12-14'
d={}
e={}
count=1
filepath1 = f'/home/ubuntu/summary/sim_sales_{today}_{current}.csv'
filepath2 = f'/home/ubuntu/summary/retailers_{today}_{current}.csv'
for hour in range(9,current+1):
    current_hour = str(hour).zfill(2)
    # Handle transition to the next day
    if current_hour == '24':
        next_date = (datetime.strptime(today, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
        current_hour = '00'
    else:
        next_date = today
    print (next_date)
    print(current_hour)
    # Get reseller_code values
    print(f"SELECT reseller_code FROM subscription WHERE created_date >= '{today} 00:00:00' AND created_date < '{next_date} {current_hour}:00:00' GROUP BY reseller_code;")
    reseller_codes = execute_query(f"SELECT reseller_code FROM subscription WHERE created_date >= '{today} 00:00:00' AND created_date < '{next_date} {current_hour}:00:00' GROUP BY reseller_code;")
 #   print(reseller_codes)
    if reseller_codes:
        for reseller_code in reseller_codes:
            reseller_code = reseller_code[0]
           # print(reseller_code)
            sim_sales = execute_query(f"SELECT count(*) FROM subscription WHERE reseller_code = '{reseller_code}' AND created_date >= '{today} 00:00:00' AND created_date < '{next_date} {current_hour}:00:00';")[0][0]
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
    
    
    files(filepath1,d)
    files(filepath2,e)
    
    for aggregator_name in d:
      d[aggregator_name]=0

    for aggregator_name in e:
      e[aggregator_name]=0
    
    



subprocess.run(['python3', '/home/ubuntu/sim_sales_reporting/hourly_mail.py'])
