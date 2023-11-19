from ReservationHeap import MinHeap
from Errors import DuplicateBookID,InvalidValue,InvalidAvailabilityStatus,EntryNotFound
from RedBlackTree import RBNode
'''
This module contains Utility functions to support operations required in the main class such as Validation Checks,
formatting issues, etc., 
'''

def validateInt(*bookIDs:[int]) -> int:
    '''
    This function is used to validate whether the given Book ID is actually an integer and not another datatype.
    
    Args:
        bookID -> The bookID which requires validation
    
    Returns:
        None
    
    Raises:
        InvalidBookID error.
    '''
    for bookID in bookIDs:
        try:
            bookID = convert_int(bookID)    
        except ValueError:
            raise InvalidValue(bookID,'Book ID')

def validate_availability_status(availabilityStatus:str):
    '''
    This fucntion will validate the value for availability status. 
    '''
    availabilityStatus = convert_lower(availabilityStatus)
    if not (availabilityStatus != 'yes') and not(availabilityStatus != 'no'):
        raise InvalidAvailabilityStatus(availabilityStatus)

def validateDuplicateBookID(bookID,rb_tree):
    if rb_tree.find_book(bookID):
        raise DuplicateBookID(bookID)

def validateReturnBookInput(patronID: int, bookID: int,rb_tree) -> RBNode:
    validateInt(patronID,bookID)
    return validate_book_ID(bookID,rb_tree)
    

def validate_book_ID(bookID, rb_tree) -> RBNode:
    validateInt(bookID)
    book = rb_tree.find_book(bookID)
    if not book:
        raise EntryNotFound(bookID,'BookID ')
    return book

def convert_lower(string):
    if type(string) == 'str':
        return string.lower()
    return str(string).lower()

def convert_int(num):
    return int(num)

def validateInsertInput(bookID:int, bookName:str, authorName:str, availabilityStatus: str, borrowedBy: [int], reservationHeap: MinHeap, rb_tree):
    '''
    This function is used to validate all the args passed to the InsertBook function.
    '''
    validateInt(bookID)
    validateDuplicateBookID(bookID,rb_tree)
    validate_availability_status(availabilityStatus=availabilityStatus)

    