import pymongo
from pymongo import MongoClient
from gridfs import GridFS

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['photo_database']
fs = GridFS(db)

# Sample data
people = [
    {'name': 'Mohammad Alashkar', 'image': 'C:/Users/A U C/Downloads/image1.png'},
    {'name': 'Andrew Aziz', 'image': 'C:/Users/A U C/Downloads/image2.png'},
    {'name': 'Omar Ashraf', 'image': 'C:/Users/A U C/Downloads/image3.png'},
]

# Insert data into MongoDB
for person in people:
    with open(person['image'], 'rb') as image_file:
        image_id = fs.put(image_file)
        person['image_id'] = image_id

    db.people.insert_one({'name': person['name'], 'image_id': person['image_id']})
