BLACK = 1
RED = 0

#Constants for availability Status.
YES = 'yes'
NO = 'no'
from graphviz import Digraph
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
    
    def print_details(self,f, found:bool = True, bookID:str = "") -> None:
        if found:
            print(f'BookID = {self.key}\nTitle = "{self.bookName}"\nAuthor = "{self.authorName}"\nAvailability = "{self.available.capitalize()}"\nBorrowedBy = {self.borrowedBy}\nReservations = {self.get_reservation_heap()}\n',file=f)
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

    def get_color_flip_count(self):
        return self.color_flip_count
    
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
        # if self.root.color != BLACK:
        #     self._update_color_flip()
        self.root.color = BLACK

    def _check_and_update_flip(self, node, new_color):
        # print(f"node.key = {node.key} node.color = {node.color}, new_color = {new_color}")
        # print(f"Old ColorFlip = {self.color_flip_count}")
        if node and node.color != new_color:
            if (node.color == RED and new_color == BLACK) or (node.color == BLACK and new_color == RED):
                self._update_color_flip()
            node.color = new_color
        #print(f"New ColorFlip = {self.color_flip_count}")

    def _inter_color_check_and_update(self,interFlipColor,node,color):
        if node in interFlipColor and interFlipColor[node] != color:
            self._update_color_flip()

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

        
    def _copy_details(self,node_to_delete,succ):
        node_to_delete.key = succ.key
        node_to_delete.bookName = succ.bookName
        node_to_delete.authorName = succ.authorName
        node_to_delete.available = succ.available
        node_to_delete.borrowedBy = succ.borrowedBy
        node_to_delete.reservationHeap = succ.reservationHeap
        
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


    
    def borrow_book(self,patronID:int, bookID: int, patronPriority: int,f) -> None:
        book = self.find_book(bookID)
        if book and book.get_availability_status() == YES: 
            print(f"Book {bookID} Borrowed by Patron {patronID}\n",file=f)
            book.set_availability_status(NO)
            book.set_borrowed_by(patronID)
        else:
            reservation = Reservation(patronID, bookID, patronPriority)
            book.reservationHeap.insert(reservation)
            print(f"Book {bookID} Reserved by Patron {patronID}\n",file=f)
            
    def return_book(self,patronID:int, bookID:int,book: RBNode,f):
        print(f"Book {bookID} Returned by Patron {patronID}\n",file=f)
        book.set_availability_status(YES)
        if book.reservationHeap.peek_min():
            newPatron = book.reservationHeap.peek_min()
            print(f"Book {bookID} Alloted to Patron {newPatron.patronID}\n",file=f)
            book.set_availability_status(NO)
            book.set_borrowed_by(newPatron.patronID)
            book.reservationHeap.remove_min()

    
            
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

    def delete_book(self, k):
        node_to_delete = self.find_book(k)

        y = node_to_delete
        y_orig_color = y.color 
        #Case 1 - Deletion of a leaf. 
        if node_to_delete.left == self.NULL and node_to_delete.right == self.NULL:
            #Change the pointers of py and node_to_delete to y
            py = node_to_delete.right
            self.transplant(node_to_delete,node_to_delete.right)
            #If Black leaf is deleted, we might need to rebalance the tree. 
            if y_orig_color == BLACK:
                self.delete_fixup(py)
            return
        #Case 2.1 Deletion of a node with one child - Left Child is empty.
        if node_to_delete.left == self.NULL:
            py = node_to_delete.right 
            self.transplant(node_to_delete, node_to_delete.right)
        #Case 2.2 Deletion of a node with one child - Right Child is empty.
        elif node_to_delete.right == self.NULL:
            py = node_to_delete.left
            self.transplant(node_to_delete, node_to_delete.left)
        
        #Case 3 - Deletion of a node with 2 children.
        else:
            #Get the Maximum node from left subtree to replace the deletion node.
            y = self.maxValueNode(node_to_delete.left)
            y_orig_color = y.color
            
            py = y.left 
            
            if y.parent == node_to_delete:
                py.parent = y
            else:
                self.transplant(y, y.left)
                y.left = node_to_delete.left
                y.left.parent = y
                
            self._copy_details(node_to_delete, y)
            self.transplant(node_to_delete, y)
            y.right = node_to_delete.right 
            y.right.parent = y 
            y.color = node_to_delete.color 
        
        if y_orig_color == BLACK:
            self.delete_fixup(py)
        else:
            if y_orig_color != y.color:
                self._update_color_flip()

    # O(logn)
    def delete_fixup(self, x):
        while x != self.root and x.color == BLACK:
            if x == x.parent.left:
                w = x.parent.right
                # type 1
                if w.color == RED:
                    self._check_and_update_flip(w,BLACK)
                    self._check_and_update_flip(x.parent,RED)
                    self._left_rotate(x.parent)
                    w = x.parent.right
                # type 2
                if w.left.color == BLACK and w.right.color == BLACK:
                    self._check_and_update_flip(w,RED)
                    x = x.parent 
                else:
                    #This is an LR rotation to handle the tree. Need to track intermediate colorFlips so we don't double count the color flips.
                    interColorFlip = {}
                    if w.right.color == BLACK:
                        interColorFlip[w.left] = w.left.color
                        self._check_and_update_flip(w.left,BLACK)
                        interColorFlip[w] = w.color
                        self._check_and_update_flip(w,RED)
                        self._right_rotate(w)
                        w = x.parent.right
                    # type 4
                    self._check_and_update_flip(w,x.parent.color)
                    self._check_and_update_flip(x.parent,BLACK)
                    self._check_and_update_flip(w.right,BLACK)
                    self._left_rotate(x.parent)
                    x = self.root
                    
            else:
                w = x.parent.left
                # type 1
                if w.color == RED:
                    self._check_and_update_flip(w,BLACK)
                    self._check_and_update_flip(x.parent,RED)
                    self._right_rotate(x.parent)
                    w = x.parent.left
                # type 2
                if w.right.color == BLACK and w.left.color == BLACK:
                    self._check_and_update_flip(w,RED)
                    x = x.parent 
                else:
                    # type 3
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

    # O(1)
    def transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v 
        else:
            u.parent.right = v
        v.parent = u.parent 

    # O(h) = O(logn) for RB trees
    def maxValueNode(self, x):
        while x.right != self.NULL:
            x = x.right
        return x