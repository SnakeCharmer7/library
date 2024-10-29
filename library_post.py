import psycopg2
from dataclasses import dataclass
from tabulate import tabulate


@dataclass
class Book:
    title: str
    author: str
    pages: int


class Library:
    """Opens a connection to the database and initializes the table if it doesn’t exist."""
    def __init__(self):
        self.conn = psycopg2.connect(dbname="library", user="postgres", password="3.14159265", host="localhost")
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS books(
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                author VARCHAR(255) NOT NULL,
                pages INT NOT NULL
            );
        ''')
        self.conn.commit()

    def add_book(self):
        """Inserts a new book into the database."""
        title = input("Podaj tytuł: ")
        author = input("Podaj autora: ")
        while True:
            try:
                pages = int(input("Podaj ilość stron: "))
                break
            except ValueError:
                print("\033[1;31mBłąd: Ilość stron musi być liczbą\033[0m")
        
        self.cur.execute('''
            INSERT INTO books (title, author, pages)
            VALUES (%s, %s, %s);
        ''', (title, author, pages))
        self.conn.commit()
        print(f"\033[1;32mDodano książkę \"{title}\"\033[0m")

    def delete_book(self):
        """Deletes a book from the database by title."""
        title = input("Podaj tytuł książki którą chcesz usunąć: ").lower()
        self.cur.execute("DELETE FROM books WHERE LOWER(title) = %s", (title,))
        if self.cur.rowcount > 0:
            self.conn.commit()
            print("\033[1;32mUsunięto książke\033[0m")
        else:
            print("\033[1;31mNie ma takiej książki\033[0m")

    def show_books(self):
        """Retrieves and displays all books in a table format."""
        self.cur.execute("SELECT title, author, pages FROM books")
        rows = self.cur.fetchall()

        if rows:
            table = [list(row) for row in rows]
            print(tabulate(table, headers=["Tytuł", "Autor", "Ilość stron"], tablefmt="grid"))
        else:
            print("\033[1;31mBrak książek w bibliotece.\033[0m")

    def search_book(self, by_what):
        """Searches the database for books by either title or author."""
        if by_what == 'author':
            author = input("Podaj autora: ").lower()
            self.cur.execute("SELECT title, author, pages FROM books WHERE LOWER(author) LIKE %s", ('%' + author + '%',))
        elif by_what == 'title':
            title = input("Podaj tytuł: ").lower()
            self.cur.execute("SELECT title, author, pages FROM books WHERE LOWER(title) LIKE %s", ('%' + title + '%',))

        rows = self.cur.fetchall()
        if rows:
            table = [list(row) for row in rows]
            print(tabulate(table, headers=["Tytuł", "Autor", "Ilość stron"], tablefmt="grid"))
        else:
            print("\033[1;31mNie znaleziono żadnej książki\033[0m")

    def __del__(self):
        """Closes the database connection when the object is destroyed."""
        self.conn.close()


def menu() -> None:
    """Displays the main menu of the library management system."""
    print("\033[1;34m1. Dodaj książkę")
    print("2. Usuń książkę")
    print("3. Pokaż książki")
    print("4. Znajdź książki")
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
                print("Na podstawie czego szukać?")
                print("\033[1;34m1. Autor")
                print("2. Tytuł\033[0m\n")
                choice2 = input("Wybierz opcję: ")
                print()
                if choice2 == '1':
                    lib.search_book('author')
                elif choice2 == '2':
                    lib.search_book('title')
                else:
                    print("\033[1;31mNieprawidłowy wybór. Spróbuj ponownie.\033[0m")
            case '5':
                print("ADIOS")
                exit()
            case _:
                print("\033[1;31mNieprawidłowy wybór. Spróbuj ponownie.\033[0m")
        input("\nNaciśnij Enter, aby kontynuować...\n")


if __name__ == "__main__":
    main()