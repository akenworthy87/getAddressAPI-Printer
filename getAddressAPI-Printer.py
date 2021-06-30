import os
from pymongo import MongoClient
# from datetime import datetime

MONGO_URI = os.environ.get('MONGODB_URI')
API_KEY = os.environ.get('API_KEY')

client = MongoClient(MONGO_URI)
db = client.getAddress.postcodes


# print(
#     db.find_one(
#         {"postcode": "NN1 3ER"}
#     ))


# 2. Request Postcode record from DB:
def lookup_postcode_in_db(postcode):
    # Attempt to find cached postcode details in DB
    record = db.find_one({"postcode": postcode})
    # Check if record found
    if record is None:
        # If not found query api
        record = query_api_for_addresses(postcode)
    # Second check to see if API lookup successful
    if not record:
        print("Postcode not found in DB or API")
    else:
        # Print addresses if record found
        print_addresses(record)


# Query getAddress API for current record (format & sorted = true)
# Store record in DB
# Add postcode and timestamp to record
# Send record to Print_Addresses()
def query_api_for_addresses(postcode):
    print(f"Calling API for {postcode}")


# 3. Print_Addresses() takes a dict of format: {addresses:[*address*:[*lines*]]}
def print_addresses(record):
    for address in record["addresses"]:
        for line in address:
            # print(line) if not blank
            if line:
                print(line)
        print()


# 1. Console Input: Ask user to provide Postcode to look up, or (q)uit
if __name__ == '__main__':
    while True:
        # print()
        postcode = input("Enter postcode to lookup, or (q)uit: ")
        # Checking if user wants to quit
        if postcode == "q":
            quit()
        # Checking if postcode isn't blank, loops back if is
        if postcode:
            lookup_postcode_in_db(postcode.upper())
