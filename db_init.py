from pymongo import MongoClient
from pymongo.errors import OperationFailure


client = MongoClient()
db = client["library"]

def init_db():
       
    if 'authors' in db.list_collection_names():
        db.drop_collection('authors')
    if 'books' in db.list_collection_names():
        db.drop_collection('books')

    db.create_collection(
        "authors",
        validator = {
            "$jsonSchema": {
                "bsonType" : "object",
                "required" : ["name", "surname", "birth_date"],
                "properties" : {
                    "name" : {"bsonType" : "string"},
                    "surname" : {"bsonType" : "string"},
                    "birth_date" : {"bsonType" : "string",
                                    "pattern" : "^\\d{2}-\\d{2}-\\d{4}$"}
                }
            }
        }
    )

    db.create_collection(
        "books",
        validator = {
            "$jsonSchema": {
                "bsonType" : "object",
                "required" : ["title", "author", "year", "genre"],
                "properties" : {
                    "title" : {"bsonType" : "string"},
                    "author" : {"bsonType" : "string"},
                    "year" : {"bsonType" : "int"},
                    "genre" : {"bsonType" : ["array", "string"]}
                }
            }
        }
    )




    

     
         
         



     


