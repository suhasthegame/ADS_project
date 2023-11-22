#Main function for our application GatorLibrary
import sys
import os
from RedBlackTree import RedBlackTree
from ReservationHeap import MinHeap
from Utils import validateInsertInput,validateInt,convert_int,convert_lower,validateReturnBookInput,validate_book_ID
#Read input file from command line argument.
fileName = sys.argv[1]

#Code to write the output to a filename inputFilename 
root, ext = os.path.splitext(fileName)
f = open(root + '_' + 'output_file.txt','w')

#Initialize the Red Black tree.

rb_tree = RedBlackTree()

#Defining the input and output functions

#PrintBook function
def PrintBook(bookID:int):
    '''
    This function prints the details of a requested book if it's present in the Library or returns None.
    
    Args: 
        bookID -> ID of the requested book from the library
    
    Returns: 
        None
        
    Raises:
        ValueError: If the bookID is not an integer.

    Examples:
        >>> PrintBook(1)
        BookID = 1
        Title = Book1
        Author = Author1
        Availability = Yes
        BorrowedBy = None
        Reservation = None
    '''
    validateInt(bookID)
    book = rb_tree.find_book(convert_int(bookID))
    if not book:
        print(f"Book {bookID} not found in the Library\n",file=f)
        return
    book.print_details(f)

#Insert Book function 
def InsertBook(bookID:int, bookName:str, authorName:str, availabilityStatus: str,borrowedBy: [int] = None, reservationHeap: MinHeap = None) -> None:
    '''
    This function is used to insert a new book with a unique bookID into the GatorLibrary Catalog.
    
    Args:
        bookID(int) -> An interger ID that uniquely identifies the book in the GatorLibrary Catalog
        bookName(str) -> The name of the book
        authorName(str) -> The author of the book
        availabilityStatus("Yes"|"No") -> A string boolean to indicate whether the book is currenlty available or not. 
        
    Returns:
        None
    
    Raises:
        Validation Errors:
            Possible Violations - 
            Duplicate BookID - book with bookID already exists in the GatorLibrary Catalog.
            Invalid BorrowedBy Format - If the borrowedBy format is violated.
            Reservation Heap - If the reservationHeap is provided and if violations are found within that reservationHeap. 
    '''
    validateInsertInput(bookID,bookName,authorName,availabilityStatus,borrowedBy,reservationHeap,rb_tree)
    bookID = int(bookID)
    availabilityStatus = convert_lower(availabilityStatus)
    rb_tree.insert(bookID=bookID,bookName=bookName,authorName=authorName,availablilityStatus=availabilityStatus, borrowedBy=borrowedBy, reservationHeap=reservationHeap)
    
#Print all books within a range
def PrintBooks(bookID1:int, bookID2:int):
    validateInt(bookID1,bookID2)
    books = rb_tree.search_books(bookID1,bookID2)
    if not books:
        print(f"No books found in range {bookID1} to {bookID2}\n",file=f)
    for book in books:
        book.print_details(f)

#Borrowing a book from GatorLibrary
def BorrowBook(patronID:int, bookID:int, patronPriority:int):
    validateInt(patronID,patronPriority,bookID)
    rb_tree.borrow_book(patronID,bookID,patronPriority,f)

#Returning a book.
def ReturnBook(patronID, bookID):
    book = validateReturnBookInput(patronID,bookID,rb_tree=rb_tree)
    rb_tree.return_book(patronID,bookID,book,f)
    
#Deleting a book from the catalog
def DeleteBook(bookID:int) -> None:
    book = validate_book_ID(bookID,rb_tree)
    #Case 1 - No reservations found 
    if book.reservationHeap.is_empty():
        print(f'Book {bookID} is no longer available\n',file=f)
    #Case 2 - Reservation is found for a single patron
    elif len(book.reservationHeap.get_patron_ids()) == 1:
        patronID = book.reservationHeap.peek_min().patronID
        print(f'Book {bookID} is no longer available. Reservation made by Patron {patronID} has been cancelled!\n',file=f)
    #Case 3 - Reservation is found for multiple patrons
    else:
        patronIDs = map(str,book.reservationHeap.get_patron_ids())
        patronIDs = ', '.join(patronIDs)
        print(f'Book {bookID} is no longer available. Reservations made by Patrons {patronIDs} have been cancelled!\n',file=f)
    rb_tree.delete_book(bookID)

#Find the closest book to the given ID from Catalog
def FindClosestBook(targetID:int) -> None:
    validateInt(targetID)
    closest = rb_tree.find_closest(targetID)
    for book in sorted(closest, key=lambda x: x.key):
        book.print_details(f)
        
    
#Get the total Nuber of Color Flips
def ColorFlipCount() -> None:
    print(f"Colour Flip Count: {rb_tree.get_color_flip_count()}\n",file=f)

#This function can be used to visualize the tree.
def VisualizeTree():
    rb_tree.visualize_tree()

#Terminate the program 
def Quit() -> None:
    print('Program Terminated!!\n',file=f)
    exit()
    


#Read input from the input_filename and execute the function.
with open(fileName, 'r') as line:
    try:
        for instruction in line.readlines():
            instruction = instruction.strip().replace(';','')
            eval(instruction)
    except Exception as e:
        print(F"ERROR OCCUREED {e}")
    finally:
        f.close()
        
    
    
    
