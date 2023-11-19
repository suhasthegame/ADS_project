import time 
class Reservation:
    def __init__(self, patronID, bookID, patronPriority):
        self.patronID = patronID
        self.priorityNumber = patronPriority
        self.booKID = bookID
        self.timeOfReservation = time.time()

    def __lt__(self, other):
        if self.priorityNumber == other.priorityNumber:
            return self.timeOfReservation < other.timeOfReservation
        return self.priorityNumber < other.priorityNumber

    def __repr__(self):
        return f"({self.patronID}, Priority: {self.priorityNumber}, Time: {self.timeOfReservation})"
    
    def get_patron_id(self):
        return self.patronID

class MinHeap:
    def __init__(self):
        self.heap = []
    
    #Method to show the items in Heap
    def print_heap(self):
        res = []
        for i in self.heap:
            res.append(i)
        return res
    
    def get_patron_ids(self):
        res = []
        for i in self.heap:
            res.append(i.get_patron_id())
        return res

    def parent(self, index):
        return (index - 1) // 2

    def left_child(self, index):
        return 2 * index + 1

    def right_child(self, index):
        return 2 * index + 2

    def has_left_child(self, index):
        return self.left_child(index) < len(self.heap)

    def has_right_child(self, index):
        return self.right_child(index) < len(self.heap)

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def insert(self, reservation):
        self.heap.append(reservation)
        self.heapify_up(len(self.heap) - 1)

    def heapify_up(self, index):
        while index > 0 and self.heap[index] < self.heap[self.parent(index)]:
            self.swap(index, self.parent(index))
            index = self.parent(index)

    def remove_min(self):
        if not self.heap:
            return None
        self.swap(0, len(self.heap) - 1)
        min_item = self.heap.pop()
        self.heapify_down(0)
        return min_item

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

    def peek_min(self) -> Reservation:
        return self.heap[0] if self.heap else None


