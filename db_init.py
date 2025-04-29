from pymongo import MongoClient
from pymongo.errors import OperationFailure

client = MongoClient()
db = client["library"]

def check_db_exists():
    return 'authors' in db.list_collection_names() and 'books' in db.list_collection_names()

def init_db():
    try:

        if 'authors' not in db.list_collection_names():
            db.create_collection(
                "authors",
                validator={
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["name", "surname", "birth_date"],
                        "properties": {
                            "name": {"bsonType": "string"},
                            "surname": {"bsonType": "string"},
                            "birth_date": {
                                "bsonType": "string",
                                "pattern": "^\\d{2}-\\d{2}-\\d{4}$"
                            }
                        }
                    }
                }
            )

        if 'books' not in db.list_collection_names():
            db.create_collection(
                "books",
                validator={
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["title", "author", "year", "genre"],
                        "properties": {
                            "title": {"bsonType": "string"},
                            "author": {"bsonType": "objectId"},
                            "year": {"bsonType": "int"},
                            "genre": {"bsonType": "string"}
                        }
                    }
                }
            )

        print("База данных инициализирована")
    except OperationFailure as e:
        print(f"Ошибка инициализации БД: {str(e)}")