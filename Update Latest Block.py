import requests
import json

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
