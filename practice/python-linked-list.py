"""
Python Linked List Implementation
DevOps / DSA Practice

Operations:
- Insert at beginning
- Insert at end
- Insert at position
- Delete a node
- Search
- Display
"""


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, data):
        """Insert a node at the beginning."""

        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data):
        """Insert a node at the end."""

        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            return

        current = self.head

        while current.next:
            current = current.next

        current.next = new_node

    def insert_at_position(self, data, position):
        """Insert a node at a zero-based position."""

        if position < 0:
            return

        if position == 0:
            self.insert_at_beginning(data)
            return

        new_node = Node(data)
        current = self.head

        for _ in range(position - 1):
            if current is None:
                return
            current = current.next

        if current is None:
            return

        new_node.next = current.next
        current.next = new_node

    def delete(self, data):
        """Delete the first node containing data."""

        if self.head is None:
            return

        if self.head.data == data:
            self.head = self.head.next
            return

        current = self.head

        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                return

            current = current.next

    def search(self, data):
        """Search for a value in the linked list."""

        current = self.head
        position = 0

        while current:
            if current.data == data:
                return position

            current = current.next
            position += 1

        return -1

    def display(self):
        """Display the linked list."""

        current = self.head
        values = []

        while current:
            values.append(str(current.data))
            current = current.next

        print(" -> ".join(values) if values else "Empty")


# --------------------------------------------------
# Example Usage
# --------------------------------------------------

if __name__ == "__main__":

    linked_list = LinkedList()

    linked_list.insert_at_end("Git")
    linked_list.insert_at_end("Docker")
    linked_list.insert_at_end("Jenkins")

    print("Initial list:")
    linked_list.display()

    linked_list.insert_at_beginning("Linux")

    print("\nAfter inserting at beginning:")
    linked_list.display()

    linked_list.insert_at_position("Kubernetes", 2)

    print("\nAfter inserting at position 2:")
    linked_list.display()

    print(
        "\nDocker found at position:",
        linked_list.search("Docker")
    )

    linked_list.delete("Jenkins")

    print("\nAfter deleting Jenkins:")
    linked_list.display()
