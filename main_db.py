from pymongo import MongoClient
from pymongo.errors import OperationFailure
from db_init import init_db, db
from greetings import say_hi, after_choice
from db_func import *

if 'authors' not in db.list_collection_names() or 'books' not in db.list_collection_names():
    init_db()

say_hi()

while True:
    choice = int(input())

    match choice: 
        case 1:
            add_author()
        case 2:
            add_book()
        case 3:
            del_by_name ()
        case 4:
            edit_book_inf()
        case 5:
            break
            
    
    after_choice()
    
        
    





