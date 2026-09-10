import colorama
from colorama import Fore, Back, Style, init
from datetime import datetime
import os



def menu():
    init(autoreset=True)
    print(Fore.CYAN + '''╔══════════════════════════════════════════════╗
║                                              ║
║        📚  LIBRARY MANAGEMENT SYSTEM  📚     ║
║                                              ║
╚══════════════════════════════════════════════╝''')
    print(Fore.GREEN + '''1. Add Book
2. View Books
3. Search Book
4. Register User
5. Issue Book
6. Exit''')
    
#Initialization

def read_book():
    """This is a function to merely read contents of a file  """
    try:
        with open("book_data.txt", "r") as f:
            book_data = f.readlines()
        return book_data
        
    except FileNotFoundError:    
        book_data = []
        return book_data
def read_user():
    try:
        with open("reg_user.txt","r")as f:
            user_data = f.readlines()
        return user_data
    except FileNotFoundError:
        user_data = []
        return user_data


def view_book():
    book_data = read_book()    
    if len(book_data) == 0:
        print(Fore.RED + "There is no Book in DataBase to View")
    else:
        for books in book_data:
            book_id,book_name,book_author,book_quantity=books.split(",")
            print(Fore.CYAN + f"Book Id: {book_id} | Book Name:{book_name} | Book Author:{book_author} | Book Quantity:{book_quantity} ")

def search_book(value):
    book_data = read_book() 
    if len(book_data) == 0:
       print(Fore.RED + "There is no Book in DataBase to Search")
    else:
       for book in book_data:
            book_id,book_name,book_author,book_quantity=book.split(",")
            if value.isdigit():
                if book_id == value:
                   print()
                   print(Fore.CYAN + f"Book Id:{book_id} | Book Name:{book_name} | Book Author:{book_author} | Book Quantity:{book_quantity} ")
                   return book
            else:
                if book_name.lower() == value.lower():
                    print()
                    print(Fore.CYAN + f"Book Id:{book_id} | Book Name:{book_name} | Book Author:{book_author} | Book Quantity:{book_quantity} ")
                    return book

def reg_user():
        user_id=input("Enter user id: ").strip()
        user_data=read_user()
        if not user_id.isdigit():
            print(Fore.RED+"User id must be digits")
            return user_id
        for i in user_data:
            if user_id in i:
                print(Fore.RED+"User id already present")
                return
        user_name=input("Enter user name: ").strip().title()
        if not user_name.replace(" ","").isalpha():
            print(Fore.RED+"User name must be alphabets")
            return user_id
        user_no=input("Enter contact no.: ").strip()
        if not user_no.isdigit() or len(user_no)!=10:
            print(Fore.RED+"Invalid contact number")
            return
        with open ("reg_user.txt","a+")as f:
            f.write(f"{user_id},{user_name},{user_no}\n")
        print(Fore.GREEN+"User added successfully")

#docstring
def add_book():
    """This is a add book Function . It takes Book Id, Book Name, Author,Quantity as input """
    book_data = read_book()
    print(Fore.GREEN + "--- ADD BOOK ---" )
    book_name = input("Enter the Book name  :")
    for i in book_data:
        if book_name in i:
            print(Fore.GREEN + "The Book Already Exists")
            print(Fore.RED + "Terminating the function Please use Update Function")
            return 10
    book_id = len(book_data) + 1
    book_author = input("Enter author Name: ")
    print(Fore.GREEN + "Book Id is :: ", book_id)
    
    error_message = Fore.RED + "Invalid quantity entered \n Please Enter a valid Value"
    while True:
        book_quantity = input("Enter Quantity :").strip()
        if book_quantity.isdigit() :
            if int(book_quantity) > 0:
                book_quantity = int(book_quantity)
                break
            else:
                print(error_message)    
        else:
            print(error_message)
    print(Fore.GREEN + f'{"\033[1mBook added successfully.\033[0m":^100}')

    with  open("book_data.txt", "a") as f:
        f.write(f"{book_id},{book_name},{book_author},{book_quantity}\n")
    
def issue_book():
    book_data=read_book()
    user_id = input("Enter a user id ")
    #User Exists or NOt Homework 
    val = input("Enter either a book id or a Book name :: ")
    book_details = search_book(val)
    for books in book_data:
        book_id,book_name,book_author,book_quantity=books.split(",")
    quantity = input("Enter Quantity :: ")
    print(f"For the User {user_id} book {book_name} has been issued on {datetime.now().strftime("%d-%m-%Y")}")


if __name__ == "__main__" :
    while True:
        menu() 
        choice = input("Enter your choice between 1 to 6 :: ")
        if choice == "1":
            add_book()
        elif choice == "2":
            view_book()
        elif choice == "3":
            val = input("Enter either a book id or a Book name :: ")
            search_book(val)
        elif choice == "4":
            reg_user()
        elif choice == "5":
            issue_book()
        elif choice == "6":
            print(Fore.CYAN + "Thank You for using our System, Visit Again")
            break
        else:
            print(Fore.RED + "Invalid Choice")