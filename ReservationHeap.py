import time 
class Reservation:
    '''
    This method is used to create a reservation node as required by the application. 
    '''
    def __init__(self, patronID, bookID, patronPriority):
        self.patronID = patronID
        self.priorityNumber = patronPriority
        self.booKID = bookID
        self.timeOfReservation = time.time()

    def __lt__(self, other):
        '''
        This method is used to break ties between the differnt patrons who have the same priority by using the First come first 
        serve algorithms. Patrons who have the same priority will be served as they are put in the queue
        '''
        if self.priorityNumber == other.priorityNumber:
            return self.timeOfReservation < other.timeOfReservation
        return self.priorityNumber < other.priorityNumber

    #Just a helper function for debugging.
    def __repr__(self):
        return f"({self.patronID}, Priority: {self.priorityNumber}, Time: {self.timeOfReservation})"
    
    #Getter method that returns the patron ID of the node. 
    def get_patron_id(self):
        return self.patronID

class MinHeap:
    '''
    This is the implementation of the minheap class which is used as a basis for the reservation heap in the RedBlackTree.
    '''
    def __init__(self):
        self.heap = []
    
    #Method to get all the items in a reservationHeap
    def print_heap(self):
        res = []
        for i in self.heap:
            res.append(i)
        return res
    #Method to get all the patronids in a reservationHeap
    def get_patron_ids(self):
        res = []
        for i in self.heap:
            res.append(i.get_patron_id())
        return res

    #Find the parent of the given index
    def parent(self, index):
        return (index - 1) // 2

    #Find the left child of the given index
    def left_child(self, index):
        return 2 * index + 1
    #Find the right child of the given index.
    def right_child(self, index):
        return 2 * index + 2

    #Check if there is a left child for the given function
    def has_left_child(self, index):
        return self.left_child(index) < len(self.heap)

    #Check if there is a right child for the given function.
    def has_right_child(self, index):
        return self.right_child(index) < len(self.heap)

    #Swap the two elements in the heap.
    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    #Method to insert a new reservation into the heap.
    def insert(self, reservation):
        self.heap.append(reservation)
        self.heapify_up(len(self.heap) - 1) #Adjust to maintain min-heap property

    #Method to adjust heap upwards from the given index
    def heapify_up(self, index):
        while index > 0 and self.heap[index] < self.heap[self.parent(index)]:
            self.swap(index, self.parent(index))
            index = self.parent(index)

    #Remove the minimum and return the min value
    def remove_min(self):
        if not self.heap:
            return None
        self.swap(0, len(self.heap) - 1)
        min_item = self.heap.pop()
        self.heapify_down(0)
        return min_item

    #method to adjust the heap downwards from the given index 
    def heapify_down(self, index):
        while self.has_left_child(index):
            smaller_child_index = self.left_child(index)
            if self.has_right_child(index) and self.heap[self.right_child(index)] < self.heap[smaller_child_index]:
                smaller_child_index = self.right_child(index)

            if self.heap[index] < self.heap[smaller_child_index]:
                break
            else:
                self.swap(index, smaller_child_index)
            index = smaller_child_index

    #Method to check who is in front of the queue.
    def peek_min(self) -> Reservation:
        return self.heap[0] if self.heap else None

    #Method to check if the heap is empty .
    def is_empty(self) -> bool:
        return len(self.heap) == 0

