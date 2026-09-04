import colorama
from colorama import Fore,Style,Back,init
from datetime import datetime
def lib_design():
    init(autoreset=True)
    print(Fore.CYAN + """============================================
||                                        ||
||       LIBRARY MANAGEMENT SYSTEM        ||
||                                        ||
============================================""")
    print(Fore.WHITE+'''1.Add Book
2.View Books
3.Search Book
4.Register User
5.Issue Book
6.Exit''')


def add_book():
    """This function takes 3 values: 1.Book id, 2.Book name, 3.Books Author, 4.Quantity as input"""
    while True:
        print(Fore.YELLOW+"---ADD BOOK---")
        error_message=Fore.RED+"\033[1mInvalid id\033[0m"
        while True:
            book_id=input("Enter book id: ").strip()
            if book_id.isdigit():
                book_id=int(book_id)
                if book_id>0:
                    print("Valid")
                    break
                else:
                    print(error_message)
            else:
                print(error_message)

        book_name=input("Enter book name: ").strip()
        book_author=input("Enter book's Author: ").strip()

        while True:
            book_quantity=input("Enter quantity: ").strip()
            if book_quantity.isdigit():
                book_quantity=int(book_quantity)
                if book_quantity>0:
                    break
                else:
                    print(error_message)
            else:
                print(error_message)
        print(Fore.GREEN+f"{'Book added sucessfully':^100}")

        with open("book_data.txt","a")as f:
            f.write(f"{book_id},{book_name},{book_author},{book_quantity}\n")
        break


def read_book():
    try:
        with open("book_data.txt","r")as f: 
            book_data=f.readlines()
        return book_data
    except FileNotFoundError:
        book_data=[]
        return book_data

def read_reg():
    try:
        with open("reg_user.txt","r")as f:
            book_data=f.readlines()
        return book_data
    except FileNotFoundError:
        book_data=[]
        return book_data

def view_book():
    book_data=read_book()
    if len(book_data)==0:
        print(Fore.RED+"No book in the database")
    else:
        for i in book_data:
            i=i.replace(" ","")
            i=i.replace(","," ").split()
            print(Fore.CYAN+f"Book Id: {i[0]} | Book Name: {i[1]} | Book Author: {i[2]} | Book Quantity: {i[3]}")

def search_book(value):
    book_data=read_book()
    if len(book_data)==0:
        print(Fore.RED+"There is no book in the database")
    else:
        if value.isdigit():
            for book in book_data:
                book_id,book_name,book_author,book_quantity=book.strip().split(",")
                if value==book_id:
                    print(Fore.LIGHTBLUE_EX+f"Book Id: {book_id} | Book Name: {book_name} | Book Author: {book_author} | Book Quantity: {book_quantity}")
                    return book_id,book_name,book_author,book_quantity
            else:
                print(Fore.RED+f"No book is registered with the id {value}")

        else:
            for book in book_data:
                book_id,book_name,book_author,book_quantity=book.strip().split(",")
                if value.lower()==book_name.lower():
                    print(Fore.LIGHTBLUE_EX+f"Book Id: {book_id} | Book Name: {book_name} | Book Author: {book_author} | Book Quantity: {book_quantity}")
                    return book_id,book_name,book_author,book_quantity
            else:
                print(Fore.RED+f"No book is registered with the name {value}")
   
            
                
def register_user():
    while True:
        # user_id=input("Enter User Id: ").strip()
        # if user_id.isdigit():
        #     user_id=int(user_id)
        #     if user_id>0:
        #         pass
        #     else:
        #         print(Fore.RED+"Invalid Id entered")
        user_name=input("Enter user's name: ").strip().title()
        user_contact=input("Enter contact number: ").strip()
        with open("reg_user.txt","r+")as f:
                    reg_user=f.readlines()
                    user_id=len(reg_user)
                    print(f"User's Id: {user_id+1}")
        if len(user_contact)!=10:
            print(Fore.RED+"Invalid number (must be 10 digits)")
        else:
            with open("reg_user.txt","a") as f:
                f.write(f"{user_id+1},{user_name},{user_contact}\n")
                print(Fore.LIGHTGREEN_EX+"User Sucessfully added")
                break

def issue_book():
    now=datetime.now().strftime("%d-%m-%Y")
    entered_user_id=input("Enter user id: ").strip()
    reg=read_reg()
    with open("reg_user.txt","r")as f:
        for user in reg:
            user_id,user_name,user_contact=user.strip().split(",")
            if entered_user_id == user_id:
                val=input("Enter either a book id or book name: ").strip()
                book_detail=search_book(val)               
                book_id,book_name,book_author,book_quantity=book_detail
                quantity=input("Enter quantity: ").strip()
                print(f"For the User {user_name}, Book Id: {book_id}, Book Name: {book_name} has been issued on: {now}")
                break
        else:
            print(Fore.RED+f"No user is registered with the id {entered_user_id}")


while True:
    lib_design()
    choice=input("Enter your choice from 1 to 6: ").strip()
    if choice=="1":
        add_book()
    elif choice=="2":
        view_book()
    elif choice=="3":
        val=input("Enter a book id or name: ").strip().lower()
        search_book(val)
    elif choice=="4":
        register_user()
    elif choice=="5":
        issue_book()
    elif choice=="6":
        break
    else:
        print(Fore.RED+"Invalid Choice entered\nEnter a number from 1 to 6")

