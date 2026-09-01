import colorama
from colorama import Fore,Style,Back,init
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
    with open("book_data.txt","r")as f: 
        book_data=f.readlines()
    return book_data



while True:
    lib_design()
    choice=input("Enter your choice from 1 to 6: ").strip()
    if choice=="1":
        add_book()
    elif choice=="2":
        print("View Books")
    elif choice=="3":
        print("Search Book")
    elif choice=="4":
        print("Register Book")
    elif choice=="5":
        print("Issue Book")
    elif choice=="6":
        print("Exit")
        break
    else:
        print(Fore.RED+"Invalid Choice entered\nEnter a number from 1 to 6")

