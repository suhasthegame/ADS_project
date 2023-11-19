BLACK = 1
RED = 0

#Constants for availability Status.
YES = 'yes'
NO = 'no'
# from graphviz import Digraph
from ReservationHeap import Reservation,MinHeap

class RBNode:
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
    
    def print_details(self, found:bool = True, bookID:str = "") -> None:
        if found:
            print(f'BookID = {self.key}\nTitle = "{self.bookName}"\nAuthor = "{self.authorName}"\nAvailability = "{self.available.capitalize()}"\nBorrowedBy = {self.borrowedBy}\nReservations = {self.get_reservation_heap()}\n')
        else:
            print(f"Book {bookID} not found in the Library\n")
    
    def get_availability_status(self):
        return self.available
    
    def set_availability_status(self,status):
        self.available = status
    
    def set_borrowed_by(self,patronID):
        self.borrowedBy = patronID
    
    def get_reservation_heap(self):
        return self.reservationHeap.get_patron_ids()
    
    
class RedBlackTree:
    def __init__(self) -> None:
        self.NULL = RBNode(None)  # NIL node
        self.NULL.color = BLACK
        self.root = self.NULL
        self.color_flip_count = 0
        self.count = 0
    def visualize_tree(self, filename='red_black_tree'):
        self.count += 1
        filename = filename + str(self.count)
        def add_nodes_edges(node, graph, nil_count=[0]):
            if node is not None and node != self.NULL:
                # Create a node with red or black fill, and white font color
                graph.node(str(node.key), label=str(node.key),
                           color='black' if node.color == BLACK else 'red',
                           style='filled', fontcolor='white')
                if node.left != self.NULL:
                    # Add the left child and an edge to it
                    add_nodes_edges(node.left, graph, nil_count)
                    graph.edge(str(node.key), str(node.left.key))
                else:
                    # Add a NIL node as the left child
                    nil_count[0] += 1
                    nil_label = f"nil{nil_count[0]}"
                    graph.node(nil_label, label="NIL", shape='box',
                               color='black', style='filled', fontcolor='white')
                    graph.edge(str(node.key), nil_label)
                if node.right != self.NULL:
                    # Add the right child and an edge to it
                    add_nodes_edges(node.right, graph, nil_count)
                    graph.edge(str(node.key), str(node.right.key))
                else:
                    # Add a NIL node as the right child
                    nil_count[0] += 1
                    nil_label = f"nil{nil_count[0]}"
                    graph.node(nil_label, label="NIL", shape='box',
                               color='black', style='filled', fontcolor='white')
                    graph.edge(str(node.key), nil_label)

        # Initialize a directed graph with some attributes
        graph = Digraph(comment='Red Black Tree', format='png')
        # Start the recursion to add nodes and edges
        add_nodes_edges(self.root, graph)
        # Save the graph to a file and do not view it immediately
        graph.render(filename, view=False)
    
    def insert(self,bookID:str, bookName:str, authorName:str, availablilityStatus:str="YES", borrowedBy:int = None, reservationHeap:[] = None) -> None:
        p = RBNode(bookID=bookID,bookName=bookName,authorName=authorName,available=availablilityStatus,borrowedBy=borrowedBy,reservationHeap=reservationHeap)
        #Case when there are no nodes in th RB tree
        if self.root == self.NULL:
            p.color = BLACK
            p.left = self.NULL
            p.right = self.NULL
            self.root = p
            return
        #Navigate the tree
        insertPosition = self.root
        while insertPosition != self.NULL:
            prevNode = insertPosition
            if p.key <= insertPosition.key:
                insertPosition = insertPosition.left
            elif p.key > insertPosition.key:
                insertPosition = insertPosition.right
        p.parent = prevNode
        p.left = self.NULL
        p.right = self.NULL
        if p.key <= prevNode.key:
            prevNode.left = p
        else:
            prevNode.right = p
        self._fix_insert(p)
    
    def _update_color_flip(self):
        self.color_flip_count += 1

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
            else:  # Mirror case: our parent is the right child
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

            if p == self.root:
                break
        self.root.color = BLACK

    def _check_and_update_flip(self, node, new_color):
        # print(f"node.key = {node.key} node.color = {node.color}, new_color = {new_color}")
        # print(f"Old ColorFlip = {self.color_flip_count}")
        if node.color != new_color:
            if (node.color == RED and new_color == BLACK) or (node.color == BLACK and new_color == RED):
                self._update_color_flip()
            node.color = new_color
        #print(f"New ColorFlip = {self.color_flip_count}")


    # Corrected rotations
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

                
    def delete_book(self, key):
        y = self.root
        node_to_delete = None
        while y != self.NULL:
            if key < y.key:
                y = y.left
            elif key > y.key:
                y = y.right
            else:
                node_to_delete = y
                break

        if node_to_delete is None:
            return  # Key not found in tree

        # Case 1: Deleting a leaf node
        if node_to_delete.left == self.NULL and node_to_delete.right == self.NULL:
            if node_to_delete.color == BLACK:
                self._fix_delete(node_to_delete)
            if node_to_delete == self.root:
                self.root = self.NULL
            elif node_to_delete == node_to_delete.parent.left:
                node_to_delete.parent.left = self.NULL
            else:
                node_to_delete.parent.right = self.NULL
            del node_to_delete  # Delete the node
        


        # Case 2: Deleting a node with one child
        elif node_to_delete.left == self.NULL or node_to_delete.right == self.NULL:
            if node_to_delete.left != self.NULL:
                child = node_to_delete.left
            else:
                child = node_to_delete.right

            # If the node to delete is black and the child is red, recolor the child to black
            if node_to_delete.color == BLACK:
                if child.color == RED:
                    child.color = BLACK
                else:
                    self._fix_delete(child)

            if node_to_delete == self.root:
                self.root = child
            elif node_to_delete == node_to_delete.parent.left:
                node_to_delete.parent.left = child
            else:
                node_to_delete.parent.right = child
            child.parent = node_to_delete.parent
            del node_to_delete  # Delete the node


        #Case 3: Deleting a node with 2 children
        else:
            if node_to_delete.left != self.NULL and node_to_delete.right != self.NULL:
                # Find the in-order successor (smallest in the right subtree)
                succ = self._minValueNode(node_to_delete.right)
                y_original_color = succ.color  # Store original color of successor
                y_original_key = succ.key

                # Copy the successor's details into node_to_delete (this node will stay)
                self._copy_details(node_to_delete, succ)

                # y is the node to be fixed, initially succ's right child
                y = succ.right if succ.parent != node_to_delete else succ

                # Delete the successor from its original position
                if succ.parent != node_to_delete:
                    if succ.right != self.NULL:
                        succ.right.parent = succ.parent
                    succ.parent.left = succ.right  # successor must be a left child
                else:
                    node_to_delete.right = succ.right  # case when successor is node_to_delete's child

                if succ.right != self.NULL:
                    succ.right.parent = succ.parent

                del succ  # Delete the successor

                # If original color of the successor was black, we may need to fix the tree
                
                if y_original_color == BLACK:
                    self._fix_delete(y)
                else:
                    if y_original_color != node_to_delete.color:
                        self._update_color_flip()
                    
    def _minValueNode(self, node):
        current = node
        while current.left != self.NULL:
            current = current.left
        return current
    
    def _copy_details(self,node_to_delete,succ):
        node_to_delete.key = succ.key
        node_to_delete.bookName = succ.bookName
        node_to_delete.authorName = succ.authorName
        node_to_delete.available = succ.available
        node_to_delete.borrowedBy = succ.borrowedBy
        node_to_delete.reservation = succ.reservation 
        
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
    
    def search_books(self, bookID1, bookID2):
        # Initialize a stack to simulate the recursion stack
        stack = []
        # Start with the root of the tree
        current = self.root
        # List to store the nodes that are within the range
        result = []
        #Handle edge case where the elements are only in left subtree or right subtree of root:
        if current != self.NULL and not (bookID1<=current.key<=bookID2):
            stack = [self.root]
            
        # Iterative in-order traversal with optimization
        while stack or current != self.NULL:
            # Move to the leftmost node within the range
            while current != self.NULL and current.key >= bookID1:
                stack.append(current)
                current = current.left

            # Check if there's no node to process
            if not stack:
                break

            # Current must be NULL at this point, so we pop the element from stack
            current = stack.pop()

            # If current node's key is within the range, add it to the result list
            if bookID1 <= current.key <= bookID2:
                result.append(current)

            # If current node's key is smaller than bookID2, we should check its right subtree
            if current.key < bookID2:
                current = current.right
            else:
                # If current node's key is greater than bookID2, no need to traverse right subtree
                current = self.NULL

        return result
    
    def borrow_book(self,patronID:int, bookID: int, patronPriority: int) -> None:
        book = self.find_book(bookID)
        if book and book.get_availability_status() == YES: 
            print(f"Book {bookID} Borrowed by Patron {patronID}\n")
            book.set_availability_status(NO)
            book.set_borrowed_by(patronID)
        else:
            reservation = Reservation(patronID, bookID, patronPriority)
            book.reservationHeap.insert(reservation)
            print(f"Book {bookID} Reserved by Patron {patronID}\n")
            
    def return_book(self,patronID:int, bookID:int,book: RBNode):
        print(f"Book {bookID} Returned by Patron {patronID}\n")
        book.set_availability_status(YES)
        if book.reservationHeap.peek_min():
            newPatron = book.reservationHeap.peek_min()
            print(f"Book {bookID} Alloted to Patron {newPatron.patronID}\n")
            book.set_availability_status(NO)
            book.set_borrowed_by(newPatron.patronID)
            book.reservationHeap.remove_min()

    
    def print_book(self,bookID1,bookID2):
        res = self.search_books(bookID1,bookID2)
        for i in res:
            i.print_details()
            
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

        # Now we print all the details of the book(s) found
        for book in sorted(closest, key=lambda x: x.key):
            book.print_details()

        
    def _fix_delete(self, x):
        while x != self.root and x.color == BLACK:
            if x == x.parent.left:
                s = x.parent.right
                if s.color == RED:
                    self._check_and_update_flip(s, BLACK)
                    self._check_and_update_flip(x.parent, RED)
                    self._left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == BLACK and s.right.color == BLACK:
                    self._check_and_update_flip(s, RED)
                    x = x.parent
                else:
                    if s.right.color == BLACK:
                        self._check_and_update_flip(s.left, BLACK)
                        self._check_and_update_flip(s, RED)
                        self._right_rotate(s)
                        s = x.parent.right

                    s.color = x.parent.color
                    self._check_and_update_flip(x.parent, BLACK)
                    self._check_and_update_flip(s.right, BLACK)
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == RED:
                    self._check_and_update_flip(s, BLACK)
                    self._check_and_update_flip(x.parent, RED)
                    self._right_rotate(x.parent)
                    s = x.parent.left

                if s.right.color == BLACK and s.left.color == BLACK:
                    self._check_and_update_flip(s, RED)
                    x = x.parent
                else:
                    if s.left.color == BLACK:
                        self._check_and_update_flip(s.right, BLACK)
                        self._check_and_update_flip(s, RED)
                        self._left_rotate(s)
                        s = x.parent.left

                    s.color = x.parent.color
                    self._check_and_update_flip(x.parent, BLACK)
                    self._check_and_update_flip(s.left, BLACK)
                    self._right_rotate(x.parent)
                    x = self.root

        x.color = BLACK
        






    


    