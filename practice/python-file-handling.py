"""
Python File Handling
DevOps / DSA Practice

Operations:
- Create a file
- Write to a file
- Read a file
- Append to a file
- Count lines
- Count words
- Process file content
"""

from pathlib import Path


FILE_NAME = "devops-practice.txt"


def write_file(filename, content):
    """Write content to a file."""
    Path(filename).write_text(content, encoding="utf-8")


def read_file(filename):
    """Read and return file content."""
    return Path(filename).read_text(encoding="utf-8")


def append_file(filename, content):
    """Append content to a file."""
    with open(filename, "a", encoding="utf-8") as file:
        file.write(content)


def count_lines(filename):
    """Count the number of lines in a file."""
    content = read_file(filename)

    if not content:
        return 0

    return len(content.splitlines())


def count_words(filename):
    """Count the number of words in a file."""
    content = read_file(filename)
    return len(content.split())


def find_keyword(filename, keyword):
    """Check whether a keyword exists in the file."""
    content = read_file(filename)
    return keyword.lower() in content.lower()


# --------------------------------------------------
# Example Usage
# --------------------------------------------------

if __name__ == "__main__":

    initial_content = """DevOps Practice
Docker
Git
Jenkins
Kubernetes
"""

    # Write
    write_file(FILE_NAME, initial_content)
    print("File created and written.")

    # Read
    print("\nFile Content:")
    print(read_file(FILE_NAME))

    # Append
    append_file(FILE_NAME, "AWS\n")
    print("Content appended.")

    # Statistics
    print("Line count:", count_lines(FILE_NAME))
    print("Word count:", count_words(FILE_NAME))

    # Keyword search
    keyword = "Docker"

    if find_keyword(FILE_NAME, keyword):
        print(f"'{keyword}' found in file.")
    else:
        print(f"'{keyword}' not found.")
