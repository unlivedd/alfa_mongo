import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from db_func import (
    add_author, add_book, del_by_name, edit_book_inf,
    get_all_authors_with_books, get_all_books
)
from db_init import init_db, check_db_exists

class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Управление библиотекой")
        self.geometry("650x450")
        
        self.create_widgets()
        
    def create_widgets(self):
        buttons = [
            ("Добавить автора", self.add_author_gui),
            ("Добавить книгу", self.add_book_gui),
            ("Удалить книгу", self.del_book_gui),
            ("Редактировать книгу", self.edit_book_gui),
            ("Показать всех авторов", self.show_authors),
            ("Показать все книги", self.show_books),
            ("Выход", self.destroy)
        ]
        
        for text, command in buttons:
            tk.Button(self, text=text, command=command, width=30).pack(pady=3)

    def add_author_gui(self):
        dialog = tk.Toplevel(self)
        dialog.title("Добавить автора")
        dialog.grab_set()
        
        fields = [
            ("Имя:", "name"),
            ("Фамилия:", "surname"),
            ("Дата рождения (ДД-ММ-ГГГГ):", "birth_date")
        ]
        
        entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(dialog, text=label).grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(dialog, width=25)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[key] = entry
        
        def save():
            try:
                data = {k: v.get().strip().lower() if k != 'birth_date' else v.get().strip() 
                       for k, v in entries.items()}
                
                if not all(data.values()):
                    raise ValueError("Все поля должны быть заполнены")
                
                add_author(
                    name=data['name'],
                    surname=data['surname'],
                    birth_date=data['birth_date']
                )
                messagebox.showinfo("Успех", "Автор успешно добавлен")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
        
        tk.Button(dialog, text="Сохранить", command=save).grid(row=len(fields), columnspan=2, pady=10)

    def add_book_gui(self):
        dialog = tk.Toplevel(self)
        dialog.title("Добавить книгу")
        dialog.grab_set()
        
        fields = [
            ("Название:", "title"),
            ("Имя автора:", "author_name"),
            ("Фамилия автора:", "author_surname"),
            ("Год издания:", "year"),
            ("Жанр:", "genre")
        ]
        
        entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(dialog, text=label).grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(dialog, width=25)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[key] = entry
        
        def save():
            try:
                data = {k: v.get().strip().lower() if k != 'year' else v.get().strip() 
                       for k, v in entries.items()}
                
                if not all(data.values()):
                    raise ValueError("Все поля должны быть заполнены")
                
                add_book(
                    title=data['title'],
                    author_name=data['author_name'],
                    author_surname=data['author_surname'],
                    year=int(data['year']),
                    genre=data['genre']
                )
                messagebox.showinfo("Успех", "Книга успешно добавлена")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
        
        tk.Button(dialog, text="Сохранить", command=save).grid(row=len(fields), columnspan=2, pady=10)

    def del_book_gui(self):
        title = simpledialog.askstring("Удаление", "Введите название книги:")
        if title:
            try:
                result = del_by_name(title.strip().lower())
                messagebox.showinfo("Успех", result)
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

    def edit_book_gui(self):
        title = simpledialog.askstring("Редактирование", "Введите название книги:")
        if title:
            dialog = tk.Toplevel(self)
            dialog.title("Редактирование")
            
            fields = [
                ("Новый год:", "year"),
                ("Новый жанр:", "genre"),
                ("ID нового автора:", "author_id")
            ]
            
            entries = {}
            for i, (label, key) in enumerate(fields):
                tk.Label(dialog, text=label).grid(row=i, column=0, padx=5, pady=5)
                entry = tk.Entry(dialog)
                entry.grid(row=i, column=1, padx=5, pady=5)
                entries[key] = entry
            
            def save():
                try:
                    data = {
                        "new_year": entries["year"].get(),
                        "new_genre": entries["genre"].get(),
                        "new_author_id": entries["author_id"].get()
                    }
                    edit_book_inf(
                        title=title.strip().lower(),
                        **{k: v for k, v in data.items() if v}
                    )
                    messagebox.showinfo("Успех", "Данные обновлены")
                    dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Ошибка", str(e))
            
            tk.Button(dialog, text="Сохранить", command=save).grid(row=3, columnspan=2)

    def show_authors(self):
        result_window = tk.Toplevel(self)
        result_window.title("Список авторов")
        
        text = tk.Text(result_window, wrap=tk.WORD, width=60, height=20)
        scroll = ttk.Scrollbar(result_window, command=text.yview)
        text.configure(yscrollcommand=scroll.set)
        
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        text.pack(expand=True, fill=tk.BOTH)
        
        try:
            authors = get_all_authors_with_books()
            if not authors:
                text.insert(tk.END, "В базе нет авторов")
                return
                
            for author in authors:
                text.insert(tk.END, f"\nАвтор: {author['author'].title()}\n")
                if author['books']:
                    text.insert(tk.END, "Книги:\n" + "\n".join(
                        [f"• {title.title()}" for title in author['books']]
                    ))
                else:
                    text.insert(tk.END, "Нет книг в базе\n")
                text.insert(tk.END, "\n" + "="*50 + "\n")
                
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def show_books(self):
        result_window = tk.Toplevel(self)
        result_window.title("Список книг")
        
        text = tk.Text(result_window, wrap=tk.WORD, width=60, height=20)
        scroll = ttk.Scrollbar(result_window, command=text.yview)
        text.configure(yscrollcommand=scroll.set)
        
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        text.pack(expand=True, fill=tk.BOTH)
        
        try:
            books = get_all_books()
            if not books:
                text.insert(tk.END, "В базе нет книг")
                return
                
            for book in books:
                text.insert(tk.END, 
                    f"\nНазвание: {book['title'].title()}\n"
                    f"Автор: {book['author'].title()}\n"
                    f"Год: {book['year']}\n"
                    f"Жанр: {book['genre'].title()}\n"
                    + "="*50 + "\n"
                )
                
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

if __name__ == "__main__":
    if not check_db_exists():
        init_db()
    app = LibraryApp()
    app.mainloop()