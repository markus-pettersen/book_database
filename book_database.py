import sqlite3
import pandas as pd
import os

def setup_database():
        ''''
        Creates the table if it does not exist already.
        Only unique column is ID because books can have the same title and 
        authors can write more than one book.
        Creates and deletes a placeholder variable so the IDs start at 3001
        Finally, populates the table with some books if it is empty
        '''
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        title TEXT,
                   	                author TEXT,
                                        qty INTEGER);
        ''')
        cursor.execute('''INSERT INTO books (title, author, qty)
                        VALUES(?, ?, ?);''', ('placeholder', 'placeholder', 0))
        cursor.execute('''
                UPDATE sqlite_sequence SET seq = 3000 WHERE NAME = 'books';
                ''')
        # delete placeholder
        cursor.execute('''DELETE FROM books WHERE id = ?''',
                        (cursor.lastrowid,))
        db.commit()
        # Check if empty
        cursor.execute('''
        SELECT * FROM books
        ''')
        empty_check = cursor.fetchone()
        # Populate the table with books if it is empty:
        if empty_check is None:
                add_original_books()

def add_original_books():
        ''''
        Adds a list of books to the table
        '''
        og_books = [
                ('A Tale of Two Cities', 'Charles Dickens', 30),
                ("Harry Potter and the Philosopher's Stone", 'J.K. Rowling', 40),
                ('The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 25),
                ('The Lord of the Rings', 'J.R.R. Tolkien', 37),
                ('Alice in Wonderland', 'Lewis Carroll', 12)
                ]
        cursor.executemany('''INSERT INTO books(title, author, qty)
                        VALUES(?, ?, ?);''', og_books)
        db.commit()

def add_book():
        ''''
        Prompts user to enter details of a new book
        User must enter an integer for quantity to complete
        '''
        new_title = input('''Enter book title
                        >>> ''')
        new_author = input('''Enter author
                        >>> ''')

        while True:
                new_quantity = input('''Enter quantity
                        >>> ''')                
                try:
                        new_quantity = int(new_quantity)
                except ValueError:
                        print('Quantity must be an integer. Try again')
                else:
                        new_entry = (new_title, new_author, new_quantity)

                        cursor.execute('''INSERT INTO books(title, author, qty)
                                        VALUES(?, ?, ?)''', new_entry)
                        db.commit()
                        print('Entry added successfully!')
                        break

def delete_book():
        '''
        Retrieves a book with the entered ID
        User can then delete the book
        '''
        delete_id = input('''Enter ID of book to delete
                        >>> ''')
        cursor.execute('''SELECT * FROM books WHERE id = ?;''', (delete_id, ))
        book = cursor.fetchone()
        if book is None:
                print(f'No records found for ID {delete_id}')
                return

        print('\tBook ID:\t', book[0])
        print('\tTitle:\t\t', book[1])
        print('\tAuthor:\t\t', book[2])
        print('\tQuantity:\t', book[3], '\n')
        print('Delete this entry? (Y/N)')
        while True:
                user_choice = input('>>> ').upper()
                if user_choice == 'Y':
                        cursor.execute('''DELETE FROM books WHERE id = ?;''', 
                                        (delete_id,))
                        db.commit()
                        print(f'{delete_id} deleted!')
                        break
                elif user_choice == 'N':
                        print('Returning to menu...')
                        break
                else:
                        print('Invalid choice - Try again')

def retrieve_book():
        ''''
        When user enters an ID, retrieves that entry from the table
        User can then update the details
        '''
        search_id = input('''Enter book ID:
                        >>> ''')
        cursor.execute('''SELECT * FROM books WHERE id = ?''',
                        (search_id,))
        book = cursor.fetchone()
        if book is None:
                print(f'No records found for ID {search_id}')
                return

        print('\tBook ID:\t', book[0])
        print('\tTitle:\t\t', book[1])
        print('\tAuthor:\t\t', book[2])
        print('\tQuantity:\t', book[3], '\n')
        update_book(book)

def update_book(book_tup):
        '''
        User has the option of changing the details of a given book
        Quantity must be an integer to continue
        '''
        (book_id, title, author, quantity) = book_tup
        print('Enter new TITLE (Press enter to leave unchanged):')
        new_title = input('>>> ')
        if new_title == '':
                new_title = title
        print('Enter new AUTHOR (Press enter to leave unchanged):')
        new_author = input('>>> ')
        if new_author == '':
                new_author = author
        print('Enter new QUANTITY (Press enter to leave unchanged):')
        while True:
                new_quantity = input('>>> ')
                if new_quantity == '':
                        new_quantity = quantity
                try:
                        new_quantity = int(new_quantity)
                except ValueError:
                        print('Quantity must be an integer. Try again')
                else:
                        new_info = (new_title, new_author, new_quantity, book_id)
                        cursor.execute('''UPDATE books
                                SET title = ?, author = ?,  qty = ?
                                WHERE id = ?;
                                ''', new_info)
                        db.commit()
                        print('Entry updated!')
                        break

def search_books():
        '''
        User can search the title and author columns and retrieve all the
        details of books that match the search term.
        Displays the results in a pandas dataframe with the ID as index.
        '''
        search_name = input('''Enter book title or author:
                        >>> ''')
        query_name = '%' + search_name + '%'
        cursor.execute('''SELECT * FROM books
                          WHERE title LIKE ?
                                OR author LIKE ?;''',
                        (query_name, query_name))
        book_results = cursor.fetchall()
        cols = ['ID', 'Title', 'Author', 'Quantity']
        if len(book_results) > 0:
                print(len(book_results), 'result(s) found')
                result_df =pd.DataFrame(book_results, columns=cols)
                result_df.set_index('ID', inplace=True)
                print(result_df)
        else:
                print(f"No results for '{search_name}'")

def display_all():
        '''
        Retrieves all the books in the database and shows them in a pandas
        dataframe.
        '''
        cursor.execute('''SELECT * FROM books'''
                        )
        book_list = cursor.fetchall()
        cols = ['ID', 'Title', 'Author', 'Quantity']
        print(len(book_list), 'result(s) found')
        result_df =pd.DataFrame(book_list, columns=cols)
        result_df.set_index('ID', inplace=True)
        print(result_df)
        print()

def reset_db():
        '''
        Restores the database to original values
        Drops the table and creates it again
        setup_database runs to restore it to original state
        '''
        print('!!!This will reset the database to original values!!!')
        confirm_reset = input('''Type YES to do this
                                >>> ''')
        if confirm_reset == 'YES':
                cursor.execute('''DROP TABLE books''')
                db.commit()
                print('Database reset')
                setup_database()
        else:
                print('Returning to menu...')

def exit_program():
        '''Closes the connection to the database and exits the program'''
        db.close()
        print('Connection to database closed!!!')
        exit()

def invalid_choice():
    '''
    Prints a message for the user when an invalid selection is entered at the
    menu
    '''
    print('Invalid choice. Try again.')

if __name__ == "__main__":

        # compilation error if the data folder does not already exist:
        data_folder = 'data'
        if not os.path.exists(data_folder):
                os.makedirs(data_folder)

        db  = sqlite3.connect('data/books.db')
        cursor = db.cursor()

        setup_database()

        menu_dict = {
                    "1": add_book,
                    "2": retrieve_book,
                    "3": delete_book,
                    "4": search_books,
                    "5": display_all,
                    "6": reset_db,
                    "0": exit_program,
                    }

        while True:
                menu_choice = input('''Select one of the follow options below:
                        1 - Enter book
                        2 - Update book
                        3 - Delete book
                        4 - Search books
                        5 - Display full inventory
                        6 - Reset database (DEBUG)
                        0 - Exit
                        >>> ''')
                choice_select = menu_dict.get(menu_choice, invalid_choice)
                choice_select()
