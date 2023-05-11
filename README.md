# Book database project
This is a project designed to be used in a small book shop. This program uses Python and SQLite to interact with a database containing information about books.
Users can use this interface to add books, delete books, update book information and search the database by name or ID number.

## Installation
This project runs in Python and requires the following modules:
* SQLite3
* Pandas

It is also necessary to have a folder called 'data' in the directory before running the program.

## Usage
User selects different options given on the menu by entering digits. Most necessary information is given in the menu. The user also has the ability to manually reset the database
to the original state.

## Updates
### 11th May 2023
* Reorganised menu to use a dictionary rather than if-else statements
* Added condtion to ensure code only runs when executed as a script