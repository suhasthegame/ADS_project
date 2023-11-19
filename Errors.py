class ValidationErrors(Exception):
    '''Base Class for Validation Errors'''
    pass

class InvalidValue(ValidationErrors):
    def __init__(self,value,varName, message = ' has to be an integer'):
        self.value = value
        self.message = varName + message
        super().__init__(self.message)
    
class DuplicateBookID(ValidationErrors):
    '''
    This error is raised when a user tries to insert a book with a bookID already present in the GatorLibrary Catalog.
    '''
    def __init__(self,value,message = 'Book ID already present in Catalog. Please use a different bookID'):
        self.value = value
        self.message = message
        super().__init__(self.message)

class EntryNotFound(ValidationErrors):
    '''
    This error is raised when a user tries to access an entry in the Library that is not present.
    '''
    def __init__(self, value, varName, message = 'No entry found for requested ') -> None:
        self.value = value
        self.message = message + str(varName) + str(value)
        super().__init__(self.message)
    
class InvalidAvailabilityStatus(ValidationErrors):
    '''
    This Error is raised when the user passess a value other than "Yes" or "No" to the 
    Availability Status parameter in insertbook.
    '''
    def __init__(self,value,message = 'Availability Status has to be either "Yes" or "No"'):
        self.value = value
        self.message = message
        super().__init__(self.message)