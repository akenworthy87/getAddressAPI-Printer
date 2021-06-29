# getAddress() API Address Printer

## Outline

As a tech test, I was given the following outline:
> We have a small task for you using the getaddress.io API (see <https://getaddress.io/>). You can use the language and database of your choice.
>
> - Write a console app that asks for a postcode.
> - Check if the postcode already exists in a database and the results are less than 24 hours old.
> - If it is not in the database, call the API and get addresses associated with the postcode – cache the results to a database
> - Print the addresses to the screen (from the API or the pre-cached data)
> - Ask for another postcode

## Planning

### Tech

Language: Python  
Database: MongoDB

I've chosen MongoDB because:

1. Mongo is built for storing JSON docs
2. It has a built in Time To Live feature to delete docs after a specified time, which will be useful for expiring results after 24 hours

### Order

The console program will execute as a continuous loop, until the user exits:

1. Console Input: Ask user to provide Postcode to look up, or (q)uit
2. Request Postcode record from DB, if exists:
    - Yes: Send record to Print_Addresses()
    - No:
      - Query getAddress API for current record (format & sorted = true)
      - Store record in DB
      - Send record to Print_Addresses()
3. Print_Addresses() takes a JSON of format: {addresses:[*address*:[*lines*]]}
    - for address in addresses
      - for line in address.formatted_address
        - print(line) if not blank
4. Loop back to start

## Setup

### Environment Vars

The Following EnVars will need setting:

| Key | Description |
|---|---|
APIKEY | Your getaddress.io API Key (<https://getaddress.io/CreateAccount>)
MONGODB_URI | MongoDB connection string
