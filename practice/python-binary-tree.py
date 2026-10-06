"""
Python Binary Tree Implementation
DevOps / DSA Practice

Operations:
- Insert
- Search
- Inorder Traversal
- Preorder Traversal
- Postorder Traversal
"""


class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, data):
        """Insert a value into the Binary Search Tree."""

        if self.root is None:
            self.root = Node(data)
            return

        self._insert(self.root, data)

    def _insert(self, node, data):
        if data < node.data:
            if node.left is None:
                node.left = Node(data)
            else:
                self._insert(node.left, data)

        elif data > node.data:
            if node.right is None:
                node.right = Node(data)
            else:
                self._insert(node.right, data)

    def search(self, data):
        """Search for a value in the tree."""

        current = self.root

        while current:
            if current.data == data:
                return True

            if data < current.data:
                current = current.left
            else:
                current = current.right

        return False

    def inorder(self, node):
        """Left → Root → Right."""

        if node:
            self.inorder(node.left)
            print(node.data, end=" ")
            self.inorder(node.right)

    def preorder(self, node):
        """Root → Left → Right."""

        if node:
            print(node.data, end=" ")
            self.preorder(node.left)
            self.preorder(node.right)

    def postorder(self, node):
        """Left → Right → Root."""

        if node:
            self.postorder(node.left)
            self.postorder(node.right)
            print(node.data, end=" ")


# --------------------------------------------------
# Example Usage
# --------------------------------------------------

if __name__ == "__main__":

    tree = BinarySearchTree()

    values = [50, 30, 70, 20, 40, 60, 80]

    for value in values:
        tree.insert(value)

    print("Inorder:")
    tree.inorder(tree.root)

    print("\n\nPreorder:")
    tree.preorder(tree.root)

    print("\n\nPostorder:")
    tree.postorder(tree.root)

    print("\n\nSearch 60:", tree.search(60))
    print("Search 100:", tree.search(100))
