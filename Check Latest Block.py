import requests
import json

def get_and_save_block_numbers():
    url = "https://compatible-intensive-frog.quiknode.pro/c568c74209dd5adf943eba3d0b2d6aea551d08ef/"

    payload = json.dumps({
        "method": "eth_blockNumber",
        "params": [],
        "id": 1,
        "jsonrpc": "2.0"
    })

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code == 200:
            response_json = response.json()
            latest_block_hex = response_json.get("result", "0x0")

            # Convert the latest block number from hexadecimal to decimal
            latest_block_decimal = int(latest_block_hex, 16)

            # Get the decimal representation of the latest 1000 block numbers
            block_numbers = list(range(latest_block_decimal, latest_block_decimal - 216000, -1))

            # Save block numbers to a text file
            with open("block_numbers.txt", "w") as file:
                for block_number in block_numbers:
                    file.write(str(block_number) + "\n")

            print("Latest 216000 block numbers in decimal have been saved to 'block_numbers.txt'")
        else:
            print(f"Error: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

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
def main(start_block, end_block):
    # Read block numbers from a text file if available
    try:
        with open("block_numbers.txt", "r") as file:
            block_numbers = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        # If the file doesn't exist, create and populate it
        get_and_save_block_numbers()
        with open("block_numbers.txt", "r") as file:
            block_numbers = [line.strip() for line in file.readlines()]

    url = "https://compatible-intensive-frog.quiknode.pro/c568c74209dd5adf943eba3d0b2d6aea551d08ef/"

    # Keep track of the last processed block number
    last_processed_block = None

    # Fetch data for each block number and store it in a list
    responses = []
    for block_number in block_numbers:
        block_number = int(block_number)
        if start_block <= block_number <= end_block:
            response = fetch_data_and_store(block_number, url)
            if response:
                responses.append(response)
            last_processed_block = block_number

        # If we reach the end block, break the loop
        if block_number == end_block:
            break

    # Write all responses to a single JSON file
    with open("api_responses.json", "w") as outfile:
        json.dump(responses, outfile, indent=4)

    # Update the block_numbers.txt file with remaining blocks
    with open("block_numbers.txt", "w") as file:
        for block_number in block_numbers[block_numbers.index(last_processed_block) + 1:]:
            file.write(str(block_number) + "\n")

    print(f"All data has been saved to 'api_responses.json'")

if __name__ == "__main__":
    # Get and save block numbers
    get_and_save_block_numbers()
    
    # Read start_block as a string from the block_numbers.txt file
    with open("block_numbers.txt", "r") as file:
        start_block_str = file.readline().strip()

    # Convert the start_block to an integer
    start_block = int(start_block_str)

    # Calculate end_block
    end_block = start_block - 216000  # Replace with your desired end block

    main(start_block, end_block)
