import pymongo

connection_string = "mongodb+srv://onlyplayxerath:iEEzRNyrBjaPPfTt@cluster0.00l13mt.mongodb.net/?retryWrites=true&w=majority"
# Connect to the MongoDB server
client = pymongo.MongoClient(connection_string)

# Select or create a database
db = client["training-python"]

# You can also authenticate if your MongoDB server requires it
# db.authenticate('your_username', 'your_password')
# Select or create a collection
collection = db["users"]


# Insert a document into the collection
data = {
    "name": "David3",
    "age": 30,
    "email": "john.doe@example.com"
}

result = collection.insert_one(data)
print(f"Inserted document with ID: {result.inserted_id}")