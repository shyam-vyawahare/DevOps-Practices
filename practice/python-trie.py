"""
Python Trie Implementation
DSA Practice

Operations:
1. Insert a word
2. Search for a word
3. Check whether a prefix exists
4. Find autocomplete suggestions

A Trie (Prefix Tree) stores words character by character.
Useful for dictionaries, autocomplete, and prefix searching.
"""


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        """Insert a word into the Trie."""

        node = self.root

        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()

            node = node.children[char]

        node.is_end_of_word = True

    def search(self, word):
        """Return True if the complete word exists."""

        node = self._find_node(word)
        return node is not None and node.is_end_of_word

    def starts_with(self, prefix):
        """Return True if any word starts with the prefix."""

        return self._find_node(prefix) is not None

    def _find_node(self, text):
        """Find the node representing a word or prefix."""

        node = self.root

        for char in text:
            if char not in node.children:
                return None

            node = node.children[char]

        return node

    def autocomplete(self, prefix):
        """Return all stored words beginning with a prefix."""

        node = self._find_node(prefix)

        if node is None:
            return []

        results = []

        def collect(current, word):
            if current.is_end_of_word:
                results.append(word)

            for char, child in sorted(current.children.items()):
                collect(child, word + char)

        collect(node, prefix)
        return results


# --------------------------------------------------
# Example Usage
# --------------------------------------------------

if __name__ == "__main__":

    trie = Trie()

    words = [
        "docker",
        "docs",
        "devops",
        "developer",
        "deployment",
        "python"
    ]

    for word in words:
        trie.insert(word)

    # Search for complete words
    print("Search 'docker':", trie.search("docker"))
    print("Search 'dock':", trie.search("dock"))

    # Check prefixes
    print("Prefix 'dev':", trie.starts_with("dev"))
    print("Prefix 'java':", trie.starts_with("java"))

    # Autocomplete suggestions
    print("Suggestions for 'de':", trie.autocomplete("de"))
    print("Suggestions for 'doc':", trie.autocomplete("doc"))
