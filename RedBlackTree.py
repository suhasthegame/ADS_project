BLACK = 1
RED = 0

#Constants for availability Status.
YES = 'yes'
NO = 'no'
#Uncomment if you want to see visual tree. 
#from graphviz import Digraph
from ReservationHeap import Reservation,MinHeap

class RBNode:
    '''
    This class is used to create a node that holds all the values necessary for a node in the Red Black Tree.
    '''
    def __init__(self, bookID: int = None, bookName:str = None, authorName:str=None, available:str=None, borrowedBy:int=None, reservationHeap:[] = None):
        self.key = bookID  # BookID
        self.bookName = bookName
        self.authorName = authorName
        self.available = available
        self.borrowedBy = borrowedBy
        self.parent = None  # parent
        self.color = RED
        self.left = None
        self.right = None
        self.reservationHeap = MinHeap() #Need to implement.
    
    def print_details(self,f, found:bool = True, bookID:str = "") -> None:
        '''
        This function is a wrapper function which prints all required details and provides support for methods like print_book and print_books.
        '''
        if found:
            print(f'BookID = {self.key}\nTitle = "{self.bookName}"\nAuthor = "{self.authorName}"\nAvailability = "{self.available.capitalize()}"\nBorrowedBy = {self.borrowedBy}\nReservations = {self.get_reservation_heap()}\n',file=f)
        else:
            print(f"Book {bookID} not found in the Library\n")
    
    
    #Getter and Setter Methods for availability status.
    def get_availability_status(self) -> str:
        return self.available
    
    def set_availability_status(self,status) -> None:
        self.available = status
    
    def set_borrowed_by(self,patronID):
        self.borrowedBy = patronID
    
    #Getter method for reservation Heap.
    def get_reservation_heap(self):
        return self.reservationHeap.get_patron_ids()
    
    
class RedBlackTree:
    '''
    This is the main RedBlack Tree Code that implements the Red Black Tree Class. 
    All the operations required for our GatorLibrary main function is supported by this class
    '''
    def __init__(self) -> None:
        self.NULL = RBNode(None)  # NIL node
        self.NULL.color = BLACK
        self.root = self.NULL
        self.color_flip_count = 0
        self.count = 0
        
    #This method is used to count the number of ColorFlips. 
    def get_color_flip_count(self):
        return self.color_flip_count
    
    #Just for Visualization( Usage - Obj.visualize_tree)
    ''' UNCOMMENT IF YOU WANT TO VISUALIZE THE TREE'''
    # def visualize_tree(self, filename='red_black_tree'):
    #     self.count += 1
    #     filename = filename + str(self.count)
    #     def add_nodes_edges(node, graph, nil_count=[0]):
    #         if node is not None and node != self.NULL:
    #             # Create a node with red or black fill, and white font color
    #             graph.node(str(node.key), label=str(node.key),
    #                        color='black' if node.color == BLACK else 'red',
    #                        style='filled', fontcolor='white')
    #             if node.left != self.NULL:
    #                 # Add the left child and an edge to it
    #                 add_nodes_edges(node.left, graph, nil_count)
    #                 graph.edge(str(node.key), str(node.left.key))
    #             else:
    #                 # Add a NIL node as the left child
    #                 nil_count[0] += 1
    #                 nil_label = f"nil{nil_count[0]}"
    #                 graph.node(nil_label, label="NIL", shape='box',
    #                            color='black', style='filled', fontcolor='white')
    #                 graph.edge(str(node.key), nil_label)
    #             if node.right != self.NULL:
    #                 # Add the right child and an edge to it
    #                 add_nodes_edges(node.right, graph, nil_count)
    #                 graph.edge(str(node.key), str(node.right.key))
    #             else:
    #                 # Add a NIL node as the right child
    #                 nil_count[0] += 1
    #                 nil_label = f"nil{nil_count[0]}"
    #                 graph.node(nil_label, label="NIL", shape='box',
    #                            color='black', style='filled', fontcolor='white')
    #                 graph.edge(str(node.key), nil_label)

    #     # Initialize a directed graph with some attributes
    #     graph = Digraph(comment='Red Black Tree', format='png')
    #     # Start the recursion to add nodes and edges
    #     add_nodes_edges(self.root, graph)
    #     # Save the graph to a file and do not view it immediately
    #     graph.render(filename, view=False)
    
    def insert(self,bookID:str, bookName:str, authorName:str, availablilityStatus:str="YES", borrowedBy:int = None, reservationHeap:[] = None) -> None:
        '''
        This method is used to insert books into the RedBlack Tree.
        '''
        p = RBNode(bookID=bookID,bookName=bookName,authorName=authorName,available=availablilityStatus,borrowedBy=borrowedBy,reservationHeap=reservationHeap)
        #Case when there are no nodes in th RB tree. Insert at root and you're done. 
        if self.root == self.NULL:
            p.color = BLACK
            p.left = self.NULL
            p.right = self.NULL
            self.root = p
            return
        #Navigate the tree to find the proper insert position.
        insertPosition = self.root
        while insertPosition != self.NULL:
            prevNode = insertPosition
            if p.key <= insertPosition.key:
                insertPosition = insertPosition.left
            elif p.key > insertPosition.key:
                insertPosition = insertPosition.right
        #Update the node's values before it can be inserted. 
        p.parent = prevNode
        p.left = self.NULL
        p.right = self.NULL
        #Decide whether it becomes the left child or the right child.
        if p.key <= prevNode.key:
            prevNode.left = p
        else:
            prevNode.right = p
        #Fix the imbalance in the RB tree if any.
        self._fix_insert(p)
    
    #Method to update the color_flip_count.
    def _update_color_flip(self):
        self.color_flip_count += 1

    #This method is used to fix any imbalances in the tree if any after the insert operation is done. 
    def _fix_insert(self, p):
        while p != self.root and p.parent.color == RED:
            # If parent is the left child
            if p.parent == p.parent.parent.left:
                uncle = p.parent.parent.right
                if uncle.color == RED:  # Case 1: Uncle is red
                    self._check_and_update_flip(uncle, BLACK)
                    if p.parent.color == RED:
                        self._check_and_update_flip(p.parent, BLACK)
                    if p.parent.parent.color == BLACK and p.parent.parent != self.root:
                        self._check_and_update_flip(p.parent.parent, RED)
                    p = p.parent.parent
                else:  # Uncle is black 
                    if p == p.parent.right:  # Case 2: Parent's right child
                        p = p.parent
                        self._left_rotate(p)
                    self._check_and_update_flip(p.parent, BLACK)
                    self._check_and_update_flip(p.parent.parent, RED)
                    self._right_rotate(p.parent.parent)
            else:  #The parent of the newly inserted node is the right child.
                uncle = p.parent.parent.left
                if uncle.color == RED:  # Case 1: Uncle is red
                    self._check_and_update_flip(uncle, BLACK)
                    self._check_and_update_flip(p.parent, BLACK)
                    self._check_and_update_flip(p.parent.parent, RED)
                    p = p.parent.parent
                else:  # Uncle is black
                    if p == p.parent.left:  # Case 2: Parent's left child
                        p = p.parent
                        self._right_rotate(p)
                    self._check_and_update_flip(p.parent, BLACK)
                    self._check_and_update_flip(p.parent.parent, RED)
                    self._left_rotate(p.parent.parent)
            #if you reached root, exit. 
            if p == self.root:
                break
        # if self.root.color != BLACK:
        #     self._update_color_flip()
        self.root.color = BLACK

    #This code will check whether the node is already the new color before flipping it, so that we don't count the 
    #duplicate color flips. 
    def _check_and_update_flip(self, node, new_color):
        # print(f"node.key = {node.key} node.color = {node.color}, new_color = {new_color}")
        # print(f"Old ColorFlip = {self.color_flip_count}")
        if node and node.color != new_color:
            if (node.color == RED and new_color == BLACK) or (node.color == BLACK and new_color == RED):
                self._update_color_flip()
            node.color = new_color

    #LEFT Rotate. This code is used to perform left_rotate fucntion useful for all types of rotations 
    # LL,LR, RL
    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NULL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    #RIGHT Rotate. This code is used to perform right_rotate fucntion useful for all types of rotations 
    # RR,LR, RL
    def _right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.NULL:
            x.right.parent = y
        x.parent = y.parent
        if y.parent is None:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x

    #This function is useful for deletion case 3, where the node to delete has 2 children. The 
    #details of a replacement node is copied onto the place of deletion.        
    def _copy_details(self,node_to_delete,pred):
        node_to_delete.key = pred.key
        node_to_delete.bookName = pred.bookName
        node_to_delete.authorName = pred.authorName
        node_to_delete.available = pred.available
        node_to_delete.borrowedBy = pred.borrowedBy
        node_to_delete.reservationHeap = pred.reservationHeap
    
    #Function to find the book in the REd Black Tree.
    def find_book(self,bookID:int) -> [RBNode | None]:
        if self.root == self.NULL:
            return None
        y = self.root
        while y != self.NULL:
            if y.key == bookID:
                return y
            elif bookID < y.key:
                y = y.left
            else:
                y = y.right
        return None
    
    #Function to search for books in the RedBlack Tree. 
    def search_books(self, bookID1, bookID2):
        stack = []
        current = self.root
        result = []

        while stack or current != self.NULL:
            # Move to the leftmost node
            while current != self.NULL:
                stack.append(current)
                current = current.left

            # Process nodes from the stack
            current = stack.pop()

            # Check and add node key if within the range
            if bookID1 <= current.key <= bookID2:
                result.append(current)

            # Move to the right subtree
            current = current.right

        return result


    #This code is used to borrow the books from the library.
    def borrow_book(self,patronID:int, bookID: int, patronPriority: int,f) -> None:
        book = self.find_book(bookID)
        #Check if book is available. IF yes, then allot it to patron
        if book and book.get_availability_status() == YES: 
            print(f"Book {bookID} Borrowed by Patron {patronID}\n",file=f)
            book.set_availability_status(NO)
            book.set_borrowed_by(patronID)
        else:
        #If book not available, put patron in reservation queue, based on the priority. 
            reservation = Reservation(patronID, bookID, patronPriority)
            book.reservationHeap.insert(reservation)
            print(f"Book {bookID} Reserved by Patron {patronID}\n",file=f)
    
    #This code is used to return the book to the library.      
    def return_book(self,patronID:int, bookID:int,book: RBNode,f):
        print(f"Book {bookID} Returned by Patron {patronID}\n",file=f)
        book.set_availability_status(YES)
        #If other patrons are there in the reservation queue, allot it to the patron with the highest priority.
        if book.reservationHeap.peek_min():
            newPatron = book.reservationHeap.peek_min()
            print(f"Book {bookID} Allotted to Patron {newPatron.patronID}\n",file=f)
            book.set_availability_status(NO)
            book.set_borrowed_by(newPatron.patronID)
            book.reservationHeap.remove_min()

    
    
    #This method is used to find the books that are closest to the given bookID        
    def find_closest(self, targetID):
        current = self.root
        closest = []
        min_diff = float('inf')

        while current != self.NULL:
            current_diff = abs(current.key - targetID)

            # If the current difference is smaller than the minimum difference found so far
            if current_diff < min_diff:
                min_diff = current_diff
                closest = [current]  # Start a new list of closest books
            elif current_diff == min_diff:
                closest.append(current)  # Add current book to the list of closest books

            # Traverse the tree towards the target ID
            if targetID < current.key:
                current = current.left
            elif targetID > current.key:
                current = current.right
            else:  # Exact match found
                closest = [current]
                break  # Can stop searching if exact match found

        return closest

    #This method is used to handling the deletion 
    def delete_book(self, k):
        #Find the node that needs to be deleted. 
        node_to_delete = self.find_book(k)

        #Store the node's details in y.
        y = node_to_delete
        y_orig_color = y.color 
        #Case 1 - Deletion of a leaf. 
        if node_to_delete.left == self.NULL and node_to_delete.right == self.NULL:
            #Change the pointers of py and node_to_delete to y
            py = node_to_delete.right
            self.node_replace(node_to_delete,node_to_delete.right)
            #If Black leaf is deleted, we might need to rebalance the tree. 
            if y_orig_color == BLACK:
                self._fix_delete(py)
            return
        #Case 2.1 Deletion of a node with one child - Left Child is empty.
        if node_to_delete.left == self.NULL:
            py = node_to_delete.right 
            self.node_replace(node_to_delete, node_to_delete.right)
        #Case 2.2 Deletion of a node with one child - Right Child is empty.
        elif node_to_delete.right == self.NULL:
            py = node_to_delete.left
            self.node_replace(node_to_delete, node_to_delete.left)
        
        #Case 3 - Deletion of a node with 2 children.
        else:
            #Get the Maximum node from left subtree to replace the deletion node.
            y = self.maxValueNode(node_to_delete.left)
            y_orig_color = y.color
            
            py = y.left 
            #If the replacement node is the immediate child of deletion node.
            if y.parent == node_to_delete:
                py.parent = y
            else:
            #If the replacement node is not the immediate child, we need to update the points to pull the deletion node out.
                self.node_replace(y, y.left)
                y.left = node_to_delete.left
                y.left.parent = y
            
            #Copy the details over to the node which was to be deleted logically, but not actually deleted. 
            self._copy_details(node_to_delete, y)
            self.node_replace(node_to_delete, y)
            y.right = node_to_delete.right 
            y.right.parent = y 
            y.color = node_to_delete.color 
        
        #We need to fix the tree in case we delete a black Node since this will casuse imbalance in the tree.
        if y_orig_color == BLACK:
            self._fix_delete(py)
        #Might need to check for color flip updatation.
        else:
            if y_orig_color != y.color:
                self._update_color_flip()

    #This is the code that to fix the imabalances in the delettion process.
    def _fix_delete(self, x):
        while x != self.root and x.color == BLACK:
            #Check if the node that was deleted was a left child
            if x == x.parent.left:
                w = x.parent.right
                #Case where you have a red sibling. 
                #This method moves the red sibling up the tree and brings a black node in it's place.
                if w.color == RED:
                    self._check_and_update_flip(w,BLACK)
                    self._check_and_update_flip(x.parent,RED)
                    self._left_rotate(x.parent)
                    w = x.parent.right
                #Case where you have a Black sibling and all it's children are black. This method changes the sibling’s color to 
                # red and moves up the tree (to x's parent) to continue the fix.
                if w.left.color == BLACK and w.right.color == BLACK:
                    self._check_and_update_flip(w,RED)
                    x = x.parent 
                else:
                #Case where you have a black sibling with atleast one red child
                #Essentially,  we perform a LR rotation.
                    if w.right.color == BLACK:
                        self._check_and_update_flip(w.left,BLACK)
                        self._check_and_update_flip(w,RED)
                        self._right_rotate(w)
                        w = x.parent.right
                    self._check_and_update_flip(w,x.parent.color)
                    self._check_and_update_flip(x.parent,BLACK)
                    self._check_and_update_flip(w.right,BLACK)
                    self._left_rotate(x.parent)
                    x = self.root
            #This is the exact same of the above cases except this will be triggered when the node that was deleted was a right child.
            else:
                w = x.parent.left
                #Case 1 - Red Sibiling, same as above. 
                if w.color == RED:
                    self._check_and_update_flip(w,BLACK)
                    self._check_and_update_flip(x.parent,RED)
                    self._right_rotate(x.parent)
                    w = x.parent.left
                #Case 2 - Black sibling and black children, same as above. 
                if w.right.color == BLACK and w.left.color == BLACK:
                    self._check_and_update_flip(w,RED)
                    x = x.parent 
                else:
                #Case 3 - Black sibling with atleast one red child - Same as above.
                #Essentially, we perform a RL rotation
                    if w.left.color == BLACK:
                        self._check_and_update_flip(w.right,BLACK)
                        self._check_and_update_flip(w,RED)
                        self._left_rotate(w)
                        w = x.parent.left
                    
                    # type 4
                    self._check_and_update_flip(w,x.parent.color)
                    self._check_and_update_flip(x.parent,BLACK)
                    self._check_and_update_flip(w.left,BLACK)
                    self._right_rotate(x.parent)
                    
                    x = self.root
        if x.color != BLACK:
            self._update_color_flip()
        x.color = BLACK

    #This method is used to help the code with moving the pointers around so we can delete the node
    def node_replace(self, py, y):
        if py.parent == None:
            self.root = y
        elif py == py.parent.left:
            py.parent.left = y 
        else:
            py.parent.right = y
        y.parent = py.parent 

    #This method finds the rightmost child in the left subtree of a node to be deleted. 
    def maxValueNode(self, x):
        while x.right != self.NULL:
            x = x.right
        return x