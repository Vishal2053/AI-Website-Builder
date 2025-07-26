from pymongo import MongoClient
import urllib.parse

# URL-encode the username and password
username = urllib.parse.quote_plus("vishal12")
password = urllib.parse.quote_plus("Vishal12@2003")
print("Encoded username:", username)
print("Encoded password:", password)
# Construct the URI with encoded credentials
uri = f"mongodb+srv://{username}:{password}@cluster0.qjnxr0s.mongodb.net/ai_website_builder?retryWrites=true&w=majority"

client = MongoClient(uri)
try:
    client.admin.command('ping')
    print("Connected successfully!")
    db = client['ai_website_builder']
    print("Collections:", db.list_collection_names())
except Exception as e:
    print("Connection error:", e)