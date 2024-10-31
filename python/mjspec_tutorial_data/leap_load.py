import json

# Specify the path to your JSON file
file_path = 'leap.json'

# Open and load the JSON file
with open(file_path, 'r') as file:
    data = json.load(file)

# Now `data` is a Python dictionary containing the JSON data
print(data)