"""
Python Stack Implementation
DevOps / DSA Practice

A Stack follows:
LIFO → Last In, First Out

Common operations:
- push()
- pop()
- peek()
- is_empty()
- size()
"""


class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        """Add an item to the top of the stack."""
        self.items.append(item)

    def pop(self):
        """Remove and return the top item."""
        if self.is_empty():
            return None

        return self.items.pop()

    def peek(self):
        """Return the top item without removing it."""
        if self.is_empty():
            return None

        return self.items[-1]

    def is_empty(self):
        """Check whether the stack is empty."""
        return len(self.items) == 0

    def size(self):
        """Return the number of items."""
        return len(self.items)

    def display(self):
        """Display the stack."""
        print("Stack:", self.items)


# --------------------------------------------------
# Example Usage
# --------------------------------------------------

if __name__ == "__main__":

    stack = Stack()

    # Push elements
    stack.push("Docker")
    stack.push("Git")
    stack.push("Jenkins")
    stack.push("Kubernetes")

    stack.display()

    # Peek
    print("Top item:", stack.peek())

    # Pop
    print("Removed:", stack.pop())

    stack.display()

    # Size
    print("Stack size:", stack.size())

    # Check empty
    print("Is empty:", stack.is_empty())
