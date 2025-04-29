from pymongo import MongoClient
from pymongo.errors import OperationFailure
from db_init import db

def add_author(name, surname, birth_date):
    try:
        res = db.authors.insert_one({
            "name": name,
            "surname": surname,
            "birth_date": birth_date
        })
        return f"Автор успешно добавлен с ID: {res.inserted_id}"
    except OperationFailure as e:
        raise Exception(f"Ошибка ввода: {str(e)}")

def add_book(title, author_name, author_surname, year, genre):
    author = db.authors.find_one({
        "name": author_name,
        "surname": author_surname
    })
    if not author:
        raise Exception("Автор не найден!")
    
    res = db.books.insert_one({
        "title": title,
        "author": author["_id"],
        "year": year,
        "genre": genre
    })
    return f"Книга успешно добавлена с ID: {res.inserted_id}"


def del_by_name(title):
    try:
        if not title:
            raise ValueError("Не указано название книги")
        result = db.books.delete_one({"title": title.lower().strip()})
        if result.deleted_count == 0:
            raise ValueError("Книга не найдена")
        return f"Удалено: {result.deleted_count} книг"
    except Exception as e:
        raise e

def edit_book_inf(title, new_year=None, new_genre=None, new_author_id=None):
    try:
        book = db.books.find_one({"title": title.lower().strip()})
        if not book:
            raise ValueError("Книга не найдена")
        
        update_data = {}
        if new_year: update_data["year"] = int(new_year)
        if new_genre: update_data["genre"] = new_genre
        if new_author_id: update_data["author"] = new_author_id
        
        if not update_data:
            raise ValueError("Нет изменений")
        
        db.books.update_one({"_id": book["_id"]}, {"$set": update_data})
        return "Данные обновлены"
    except Exception as e:
        raise e

def get_all_authors_with_books():
    authors = db.authors.find()
    result = []
    for author in authors:
        books = db.books.find({"author": author["_id"]})
        book_titles = [book["title"] for book in books]
        result.append({
            "author": f"{author['name'].title()} {author['surname'].title()}",
            "books": book_titles
        })
    return result

def get_all_books():
    return list(db.books.aggregate([{
        "$lookup": {
            "from": "authors",
            "localField": "author",
            "foreignField": "_id",
            "as": "author_info"
        }},
        {"$unwind": "$author_info"},
        {"$project": {
            "title": 1,
            "year": 1,
            "genre": 1,
            "author": {"$concat": ["$author_info.name", " ", "$author_info.surname"]}
        }}
    ]))    

