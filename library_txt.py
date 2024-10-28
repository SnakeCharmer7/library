from tabulate import tabulate
from dataclasses import dataclass
import os


FILENAME = r'OOP\library.txt'


@dataclass
class Book:
    title: str
    author: str
    pages: int


class Library:
    """Represents a library containing a collection of books.

    Attributes:
        books (list): A list of Book objects in the library.
    """
    def __init__(self):
        """
        Initializes the library with an empty list of books.
        """
        self.books = self.load_books_from_file()

    def save_books_to_file(self):
        with open(FILENAME, 'w', encoding='utf-8') as stream:
            for book in self.books:
                stream.write(f"{book.title}, {book.author}, {book.pages}\n")

    def load_books_from_file(self) -> list[Book]:
        if not os.path.exists(FILENAME):
            return []
        
        with open(FILENAME, 'r', encoding='utf-8') as stream:
            lines = stream.readlines()

        books = []
        for line in lines:
            if line.strip():
                title, author, pages = line.strip().split(", ")
                books.append(Book(title, author, int(pages)))
        return books

    def add_book(self) -> None:
        """
        Adds a new book to the library based on user input.
        """
        title = input("Podaj tytuł: ")
        author = input("Podaj autora: ")
        while True:
            try:
                pages = int(input("Podaj ilość stron: "))
                break
            except ValueError:
                print("\033[1;31mBłąd: Ilość stron musi być liczbą\033[0m")
        
        new_book = Book(title, author, pages)
        self.books.append(new_book)
        self.save_books_to_file()
        print(f"\033[1;32mDodano książkę \"{title}\"\033[0m")

    def delete_book(self) -> None:
        """
        Removes a book from the library based on the title provided by the user.
        If the book is not found, informs the user.
        """
        title = input("Podaj tytuł książki którą chcesz usunąć: ").strip().lower()

        for book in self.books:
            if  title == book.title.strip().lower():
                self.books.remove(book)
                self.save_books_to_file()
                print("\033[1;32mUsunięto książke\033[0m")
                return
        print("\033[1;31mNie ma takiej książki\033[0m")

    def show_books(self) -> None:
        """
        Displays all the books currently in the library.
        If the library is empty, informs the user.
        """
        if not self.books:
            print("\033[1;31mBrak książek w bibliotece.\033[0m")
            return

        table = [[book.title, book.author, book.pages] for book in self.books]
        print(tabulate(table, headers=["Tytuł", "Autor", "Liczba stron"], tablefmt="grid"))

    def search_by_author(self) -> None:
        """
        Searches for books by a given author, provided by the user.
        Displays results in tabulated form.
        If no books are found, informs the user.
        """
        author = input("Podaj autora: ").lower()
        found_books = [book for book in self.books if author in book.author.lower()]

        if found_books:
            table = [[book.title, book.author, book.pages] for book in found_books]
            print(tabulate(table, headers=["Tytuł", "Autor", "Ilość stron"], tablefmt="grid"))
        else:
            print("\033[1;31mNie ma takiego autora\033[0m")


def menu() -> None:
    print("\033[1;34m1. Dodaj książkę")
    print("2. Usuń książkę")
    print("3. Pokaż książki")
    print("4. Znajdź książki na podstawie autora")
    print("5. Wyjdź z biblioteki\033[0m")


def main() -> None:
    lib = Library()

    print("\n\033[1;32m*** Witaj w bibliotece ***\033[0m")
    while True:
        menu()
        choice = input("\nWybierz opcję: ")
        print()
        match choice:
            case '1':
                lib.add_book()
            case '2':
                lib.delete_book()
            case '3':
                lib.show_books()
            case '4':
                lib.search_by_author()
            case '5':
                print("ADIOS")
                exit()
            case _:
                print("\033[1;31mNieprawidłowy wybór. Spróbuj ponownie.\033[0m")
        input("\nNaciśnij Enter, aby kontynuować...\n")


if __name__ == "__main__":
    main()