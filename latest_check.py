import requests
import json

def fetch_data_and_store(block_number, url):
    payload = json.dumps({
        "method": "eth_getBlockReceipts",
        "params": [
            block_number
        ],
        "id": 1,
        "jsonrpc": "2.0"
    }) 
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        # Make a request to the API
        response = requests.post(url, headers=headers, data=payload)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            response_json = response.json()

            return response_json

        else:
            print(f"Error: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Read block numbers from a text file
with open("continue.txt", "r") as file:
    block_numbers = [line.strip() for line in file.readlines()]

url = "https://compatible-intensive-frog.quiknode.pro/c568c74209dd5adf943eba3d0b2d6aea551d08ef/"

# Fetch data for each block number and store it in a list
responses = []
for block_number in block_numbers:
    response = fetch_data_and_store(block_number, url)
    if response:
        responses.append(response)

# Read existing data from the JSON file
existing_data = []
with open("api_responses.json", "r") as file:
    existing_data = json.load(file)

# Append new responses to the existing data
existing_data.extend(responses)

# Write the updated data back to the JSON file
with open("api_responses.json", "w") as outfile:
    json.dump(existing_data, outfile, indent=4)

print(f"All data has been appended to 'api_responses.json'")







































# latest_block_decimal = int("0x1179f50", 16)
# print(latest_block_decimal)