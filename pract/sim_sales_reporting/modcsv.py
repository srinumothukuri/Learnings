import csv

# Function to check if a name exists in a specific column
def name_exists(name, column_index, data):
    for row in data:
        if row[column_index] == name:
            return True
    return False

# Function to add values from the dictionary to the corresponding names
def add_values_to_csv(names_values_dict, column_index, data):
    header = data[0]
    print(header)
    header.append('09:00')  # Replace 'New Column Header' with your header name

    for row in data[1:]:
        print(row)
        name = row[column_index]
        if name in names_values_dict:
            value = names_values_dict[name]
#            row.append(value)
            if len(row)==1:
               for i in range(num_columns-1):
                   row.append(0)
               row.append(value)
            else:
                row.append(value)
        else:
            row.append('')  # If no value exists for the name, add an empty string or any default value

# Open the existing CSV file
existing_file = '/home/ubuntu/summary/king.csv'
#names_values = {'trade-lance_ltd.': 1, 'finconnect_limited': 10, 'sai_pali641': 4, 'aircom_technologies': 2, 'mughecom_technologies': 1, 'emerald_global': 1}

#names_values = {'finconnect_limited': 27, 'mughecom_technologies': 9, 'trade-lance_ltd.': 1, 'agents': 2, 'aperture_technologies': 3, 'sai_pali641': 5, 'teqtronix_solutions': 2, 'emerald_global': 2, 'aircom_technologies': 5}
#names_values = {'sai_pali641': 18, 'finconnect_limited': 50, 'mughecom_technologies': 14, 'aperture_technologies': 5, 'trade-lance_ltd.': 1, 'agents': 2, 'teqtronix_solutions': 6, 'emerald_global': 2, 'aircom_technologies': 8}

names_values = {'sai_pali641': 25, 'finconnect_limited': 66, 'mughecom_technologies': 22, 'aperture_technologies': 7, 'trade-lance_ltd.': 2, 'agents': 3, 'aircom_technologies': 11, 'teqtronix_solutions': 6, 'emerald_global': 2}

# Replace with your dictionary

with open(existing_file, mode='r') as file:
    csv_reader = csv.reader(file)
    data = list(csv_reader)
    print(data)

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
