"""
Python Queue Implementation
DevOps / DSA Practice

A Queue follows:
FIFO → First In, First Out

Common operations:
- enqueue()
- dequeue()
- front()
- is_empty()
- size()
"""


from collections import deque


class Queue:
    def __init__(self):
        self.items = deque()

    def enqueue(self, item):
        """Add an item to the rear of the queue."""
        self.items.append(item)

    def dequeue(self):
        """Remove and return the front item."""
        if self.is_empty():
            return None

        return self.items.popleft()

    def front(self):
        """Return the front item without removing it."""
        if self.is_empty():
            return None

        return self.items[0]

    def is_empty(self):
        """Check whether the queue is empty."""
        return len(self.items) == 0

    def size(self):
        """Return the number of items."""
        return len(self.items)

    def display(self):
        """Display the queue."""
        print("Queue:", list(self.items))


# --------------------------------------------------
# Example Usage
# --------------------------------------------------

if __name__ == "__main__":

    queue = Queue()

    # Add elements
    queue.enqueue("Git")
    queue.enqueue("Docker")
    queue.enqueue("Jenkins")
    queue.enqueue("Kubernetes")

    queue.display()

    # Front item
    print("Front item:", queue.front())

    # Remove item
    print("Removed:", queue.dequeue())

    queue.display()

    # Size
    print("Queue size:", queue.size())

    # Check empty
    print("Is empty:", queue.is_empty())
