import os
from pymongo import MongoClient
import requests
from datetime import datetime
import re

# These Envars are crucical to function, so throws error if not found
try:
    MONGO_URI = os.environ.get('MONGODB_URI')
    API_KEY = os.environ['APIKEY']
except KeyError as e:
    print(f"ERROR: Environment variable: {e} is not set")
    quit()

client = MongoClient(MONGO_URI)
db = client.getAddress.postcodes


def lookup_postcode_in_db(postcode):
    ''' Request Postcode record from DB '''
    # Attempt to find cached postcode details in DB
    record = db.find_one({"postcode": postcode})
    # Check if record found
    if record is None:
        # If not found, query api
        record = query_api_for_addresses(postcode)
    else:
        print("Retrieved cached record\n")
    # Second check to see if API lookup successful
    if not record:
        print("Postcode not found in DB or API")
        return
    else:
        # Print addresses if record found
        print_addresses(record)


def query_api_for_addresses(postcode):
    ''' Query getAddress API for current record (format & sorted = true) '''
    print(f"Calling API for {postcode}")

    endpoint = f"https://api.getAddress.io/find/{postcode}"
    query_params = {
        "api-key": API_KEY,
        "format": "true",
        "sorted": "true",
    }
    try:
        response = requests.get(endpoint, params=query_params)
    except requests.ConnectionError:
        print(f"Unable to connect to: '{endpoint}'")
        return None

    status_code = response.status_code
    response = response.json()
    if status_code == 200:
        cache_response_to_db(response, postcode)
        return response
    # Displays error if valid response not received
    else:
        print(f"Response Error {status_code}: {response['Message']}")
        return None


def cache_response_to_db(response, postcode):
    ''' Takes API response,
        amends postcode and timestamp to record,
        inserts into DB
    '''
    # Add postcode and timestamp to record
    response["postcode"] = postcode
    response["cached_date"] = datetime.utcnow()
    # Store record in DB
    db.insert_one(response)


def print_addresses(record):
    ''' Takes a dict of format: {addresses: [*address*: [*lines*]]}

        Iterates and prints lines in address,
        with blank space between addresses
    '''
    if not record["addresses"]:
        print("No addresses in record")
    for address in record["addresses"]:
        for line in address:
            # print(line) if not blank
            if line:
                print(line)
        print()


def parse_postcode(postcode):
    ''' Changes to UPPERCASE and converts postcode to format: AA99 9AA '''
    postcode = postcode.replace(' ', '').upper()
    postcode = postcode[:-3] + " " + postcode[-3:]
    return postcode


def validate_postcode(postcode):
    ''' Checks if input matches expected patterns for postcodes '''
    if re.match(r"^[A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2}$", postcode):
        return True
    else:
        print(f"'{postcode}' does not appear to be a valid postcode")
        return False


# Loops around and asks user to provide Postcode to look up, or (q)uit
if __name__ == '__main__':
    while True:
        postcode = input("Enter postcode to lookup, or (q)uit: ").strip()
        # Checking if user wants to quit
        if postcode.lower() in ["q", "quit"]:
            quit()
        postcode = parse_postcode(postcode)
        # Checking if postcode isn't blank, loops back if is
        if validate_postcode(postcode):
            lookup_postcode_in_db(postcode)
