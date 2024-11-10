from pymongo import MongoClient
# Replace these with your actual username, password, database name, and host details
database_name = 'my_database'

# Create the MongoDB connection string
# It's important to URL-encode your password if it contains special characters
connection_string = "mongodb://db_admin:bveD%25WPvvsKlA9uKbXjT*wBUg*CZ7NeP!MJ7%26K26n7U@5.tcp.ngrok.io:27780/?authMechanism=DEFAULT"

# Connect to the MongoDB server
client = MongoClient(connection_string)

# Select the database
db = client[database_name]

# Select the 'species' collection
species_collection = db['planets']

# Update operation
update_result = species_collection.update_many(
    {},  # An empty filter matches all documents
    {
        '$set': {'civ_info': {}},  # Set 'civ_info' to an empty dictionary
        '$unset': {'civilization': "", 'civilization_emerging': ""}  # Remove 'generation' and 'generation_emerging'
    }
)
