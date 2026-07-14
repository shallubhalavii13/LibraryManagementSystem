import os
from datetime import datetime , timedelta
from abc import ABC, abstractmethod

class Book:
    def __init__(self, book_id,bookname,author,isbn,quantity):
        self.book_id = str(book_id)
        self.bookname = bookname
        self.author = author
        self.isbn = isbn
        self.quantity = quantity
        

    def __str__(self):
        
        return f"Book id: '{self.book_id}''{self.bookname}' by '{self.author}' ISBN: {self.isbn} - Copies left: {self.quantity}"

class Member:
    def __init__(self,member_id,name,phoneno):
        self.member_id = member_id
        self.name = name
        self.phoneno = phoneno
        self.issued_book = {}
        self.total_fines = 0.0

    def __str__(self):
        return f"Member ID: {self.member_id} - Name: {self.name} - Phone No: {self.phoneno} - Books Issued: {len(self.issued_book)} "
    
class Library:
    def __init__(self,fine_rate_per_day = 5.00):
        self.books = {}
        self.members = {}
        self.load_books()
        self.fine_rate_per_day = fine_rate_per_day
        
    def load_books(self):
        try:
            
            with open("books.json", "r") as f:
                data = json.load(f)
                for b_id, b in data.items():
                    self.books[b_id] = Book(b_id, b['bookname'], b['author'], b['isbn'], b['quantity'])
        except (FileNotFoundError, json.JSONDecodeError):
            self.books = {}  

    def add_book(self,bookID,bookname,author,isbn,quantity):
        if bookID in self.books:
            print(f"\n ERROR: A Book with ID {bookID} already exists.")
        else:
            self.books[bookID] = Book(bookID,bookname,author,isbn,quantity)
            print(f"{bookname.capitalize()} is added to the Library.")

            json_book = {}
            for b_id,book in self.books.items():
                json_book[b_id] = {
                    "bookname": book.bookname,
                    "author": book.author,
                    "isbn": book.isbn,
                    "quantity": book.quantity
                                        }

            with open("books.json","w") as f:
                for book in self.books.values():
                    json.dump(json_book, f, indent=4)

    def view_book(self):
    
        if not self.books:
            print("The Library is currently empty. ")
            return
        else:
            print("--------Library Catalog--------")
            for book in self.books.values():
                print(book)
                
    def search_book(self,search):
        if search in self.books.values():
            book = self.books[search]
            print(f"{Book.book_id} - {Book.bookname} - {Book.author} - {Book.isbn} - {Book.quantity}")
            return
        found_any = False
        for book in self.books.values():
            if (search in book.bookname.lower()) or (search in book.author.lower()):
                self._print_book_details(book)
                found_any = True
            
        if not found_any:
            print(f"\n❌ No books found matching: '{search}'")
        
    def add_member(self,memberID,membername,phoneno):
        if memberID in self.members:
            print(f"\n ERROR: A Member with ID {memberID} already exists.")
        else:
            self.members[memberID] = Member(memberID,membername, phoneno)
            print(f"{membername.capitalize()} is added.")
        
    def view_member(self):
        if not self.members:
            print("there are no members.")
            return
        else:
            print("----Members----")
            for members in self.members.values():
                print(members)
            
    def issue_book(self,member_id,book_id):

        # validation check
        # check if member exists
        member = self.members.get(member_id)
        if not member:
            print("Member ID not found.")
            return
        
        # check if book exists
        book = self.books.get(book_id)
        if not book:
            print("Book not found.")
            return

        # check if book is already borrowed
        if book_id in Member.issued_book:
            print(f"Sorry, {bookname} is already issued. ")
            return
        
        if Book.quantity == 0:
            print(f"Sorry, {bookname} is currently out of stock!")
            return
        
        # issue the book and reduce the quantity
        Book.quantity -= 1
        due_date = datetime.now() + timedelta(days=14) # 14 days issue period
        Member.issued_book[book_id]  = due_date

        print(f"Success! '{bookname}' issued to {Member.name}.")
        print(f"Remaining copies in the Library: {Book.quantity}")
    
    def return_book(self,member_id,book_id, mock_return_date = None):
        member = self.members.get(member_id)
        book = self.books.get(book_id)

        if not member or not book:
            print("ERROR: Invalid Member or Book id. ")
        
        # Determine return date (use mock date if testing, else use Today)
        return_date = mock_return_date if mock_return_date else datetime.now()
        due_date = Member.issued_book[book_id]

        #calculate fines 
        fine = 0.0
        if return_date > due_date:
            days_late = (return_date - due_date).days
            fine = days_late * self.fine_rate_per_day
            print(f"LATE RETURN: This book is {days_late} days overdue")
            print(f"Fine Added: ₹{fine:.2f} (Rate: {self.fine_rate_per_day:.2f}/day)")

        # process the return and increase the quantity
        Book.quantity += 1
        del Member.issued_book[book_id]

        print(f"Success: '{bookname}' returned by {Member.name}.")
        

if __name__ == "__main__":
    library  = Library()
   

    while True:
        print("---------LIBRARY MENU----------")
        print("1.Add Book")
        print("2.Search Book")
        print("3.View Books")
        print("4.Add Member")
        print("5.View Members")
        print("6.Issue Book")
        print("7.Return Book")
        print("8.Reserve Book")
        print("9.Check Availability")
        print("10.View Issued Books")
        print("11.View Reservations")
        print("12.Exit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            bookID = int(input("Enter Book ID: "))
            bookname = input("Enter new book Title: ")
            author = input("Enter Author: ")
            isbn = int(input("Enter ISBN: "))
            quantity = int(input("Enter Quantity: "))

            if bookID and bookname and author and isbn and quantity:
                library.add_book(bookID,bookname,author,isbn,quantity)
            else:
                print("ERROR: All Fields are required.")

        elif choice == 2:
            search = input("Enter book ID, Title, Author to search: ").strip()
            library.search_book(search)
            

        elif choice == 3:
            
            ch = input("You wants to view book (y/n) : ")
            library.view_book()


        elif choice == 4:
            memberID = int(input("Enter member Id: "))
            membername = input("Enter your Name: ")
            phoneno = input("enter your Phone no: ")
            

            if memberID and membername and phoneno:
                library.add_member(memberID,membername,phoneno)
            else:
                print("ERROR: All Fields are required.")

        elif choice == 5:
            # print("-----Members-----")
            library.view_member()

        elif choice == 6:
            memberID = int(input("Enter your ID: "))
            bookID = int(input("enter book ID: "))
            
            library.issue_book(bookID)

        elif choice == 7:
            library.return_book()

        elif choice == 8:
            library.reserve_book()

        elif choice == 9:
            library.check_availability()

        elif choice == 10:
            library.view_issued_books()

        elif choice == 11:
            library.view_reservations()

        elif choice == 12:
            print("Thanks for using us")
            break
        else:
            print ("Invalid choice\nplease enter again...")