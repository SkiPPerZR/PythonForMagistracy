from typing import List, Dict
from pydantic import BaseModel, EmailStr, validator
from functools import wraps


class BookNotAvailable(Exception):
    def __init__(self, message: str):
        super().__init__(message)


def log_operation(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Выполняется операция: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Операция {func.__name__} завершена\n")
        return result
    return wrapper


class Book(BaseModel):
    title: str
    author: str
    year: int
    available: bool
    categories: List[str]

    @validator('categories')
    def validate_categories(cls, v):
        if not v:
            raise ValueError("Категории не могут быть пустыми")
        return v


class User(BaseModel):
    name: str
    email: EmailStr
    membership_id: str


class Library(BaseModel):
    books: List[Book] = []
    users: List[User] = []

    def total_books(self) -> int:
        return len(self.books)


@log_operation
def add_book(library: Library, book: Book) -> None:
    library.books.append(book)
    print(f"Книга '{book.title}' добавлена в библиотеку.")


@log_operation
def find_book(library: Library, title: str) -> Book | None:
    for book in library.books:
        if book.title.lower() == title.lower():
            print(f"Найдена книга: {book.title}")
            return book
    print("Книга не найдена.")
    return None


@log_operation
def is_book_borrow(library: Library, title: str) -> Book:
    book = find_book(library, title)
    if not book:
        raise BookNotAvailable(f"Книга '{title}' не найдена в библиотеке.")
    if not book.available:
        raise BookNotAvailable(f"Книга '{title}' недоступна для выдачи.")
    book.available = False
    print(f"Книга '{book.title}' выдана пользователю.")
    return book


@log_operation
def return_book(library: Library, title: str) -> None:
    book = find_book(library, title)
    if book:
        book.available = True
        print(f"Книга '{book.title}' возвращена в библиотеку.")


if __name__ == "__main__":
    library = Library()

    user1 = User(name="Иван Петров", email="ivan.petrov@example.com", membership_id="U001")
    library.users.append(user1)

    book1 = Book(title="Преступление и наказание", author="Ф. Достоевский", year=1866, available=True, categories=["Классика", "Роман"])
    book2 = Book(title="Мастер и Маргарита", author="М. Булгаков", year=1967, available=True, categories=["Фантастика", "Роман"])
    book3 = Book(title="1984", author="Дж. Оруэлл", year=1949, available=False, categories=["Антиутопия", "Политика"])

    add_book(library, book1)
    add_book(library, book2)
    add_book(library, book3)

    print(f"Всего книг в библиотеке: {library.total_books()}\n")

    try:
        is_book_borrow(library, "1984")
    except BookNotAvailable as e:
        print(f"Ошибка: {e}\n")

    is_book_borrow(library, "Мастер и Маргарита")
    return_book(library, "Мастер и Маргарита")
