from pymongo import MongoClient
from pymongo.errors import OperationFailure
from db_init import db

def add_author():
        try:
            name = input("Введите имя автора: ").strip().lower()
            surname = input("Введите фамилию автора: ").strip().lower()
            birth_date = input("Введите дату рождения автора в формате ДД-ММ-ГГГГ: ")

            res = db.authors.insert_one({
                "name" : name,
                "surname" : surname,
                "birth_date" : birth_date
        })
            print(f"Автор успешно добавлен с ID: {res.inserted_id}")
        except OperationFailure as e:
            print(f"Ошибка ввода: {str(e)}")

def add_book():
    title = input("Введите название книги: ").strip().lower()
    author_name = input("Введите имя автора: ").strip().lower()
    author_surname = input("Введите фамилию автора: ").strip().lower()

    author = db.authors.find_one({
         "name" : author_name,
         "surname" : author_surname
    })

    if not author:
         print("Автор не найден. Сначала добавьте автора!")
         return 0
    
    year = int(input("Введите год издания: "))
    genre = input("Введите жанр: ")
        
    res = db.books.insert_one({
        "title": title,
        "author": author["_id"],
        "year": year,
        "genre": genre
        })
    print(f"Книга успешно добавлена с ID: {res.inserted_id}")


def del_by_name():
    try:
        if (title := input("Название книги для удаления: ").strip().lower()) \
            and (result := db.books.delete_one({"title": title})):
            print(f"Удалено: {result.deleted_count}")
        else: print("Книга не найдена")
    except Exception as e: print(f"Ошибка: {e}")
        


def edit_book_inf():
    try:
        if not (book := db.books.find_one({
            "title": input("Название книги для редактирования: ")})):
            return print("Книга не найдена")
        
        update_data = {}
        if (year := input(f"Год [{book.get('year', '')}]: ").strip()): update_data["year"] = int(year)
        if (genre := input(f"Жанр [{book.get('genre', '')}]: ").strip()): update_data["genre"] = genre
        
        if input("Изменить автора? (y/n): ").lower() == 'y':
            author = db.authors.find_one({"name": input("Имя автора: ").strip(), "surname": input("Фамилия автора: ").strip()})
            update_data["author"] = author["_id"] if author else print("Автор не найден") or None

        if not update_data: return print("Нет изменений")
        result = db.books.update_one({"_id": book["_id"]}, {"$set": update_data})
        print("Успешно" if result.modified_count else "Не изменено")
        
    except ValueError: print("Ошибка числа")
    except Exception as e: print(f"Ошибка: {e}")
     

