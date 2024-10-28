from tabulate import tabulate
from dataclasses import dataclass


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
        self.books = []

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
        print(f"\033[1;32mDodano książkę \"{title}\"\033[0m")

    def delete_book(self) -> None:
        """
        Removes a book from the library based on the title provided by the user.
        If the book is not found, informs the user.
        """
        title = input("Podaj tytuł książki którą chcesz usunąć: ")
        for book in self.books:
            if  title.lower() == book.title.lower():
                self.books.remove(book)
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
        
        table = [book for book in self.books]
        print(tabulate(table, headers=["Tytuł", "Autor", "Ilość stron"], tablefmt="grid"))

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

lib = Library()
book1 = Book("Pan Tadeusz", "Adam Mickiewicz", 376)
book2 = Book("Dziady", "Adam Mickiewicz", 288)
book3 = Book("Wiedźmin", "Andrzej Sapkowski", 3000)
lib.books.append(book1)
lib.books.append(book2)
lib.books.append(book3)


def main() -> None:
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