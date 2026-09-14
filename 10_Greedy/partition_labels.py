"""
Partition Labels

Partition a string into as many parts as possible so that
each letter appears in at most one part.

Greedy Strategy:
    Record the last occurrence of every character.
    While scanning the string, extend the current partition
    until every character inside it has reached its final
    occurrence.

Time Complexity:
    O(n)

Space Complexity:
    O(k), where k is the number of distinct characters.
"""


def partition_labels(s):
    """
    Return the sizes of the partitions.

    Args:
        s: Input string.

    Returns:
        List containing the size of each partition.
    """

    # Store the last position of every character.
    last_occurrence = {}

    for i, char in enumerate(s):
        last_occurrence[char] = i

    partitions = []

    partition_start = 0
    partition_end = 0

    for i, char in enumerate(s):

        # The current partition must extend far enough
        # to include the character's final occurrence.
        partition_end = max(
            partition_end,
            last_occurrence[char]
        )

        # Every character in this partition has now
        # reached its final occurrence.
        if i == partition_end:
            partition_size = i - partition_start + 1
            partitions.append(partition_size)

            partition_start = i + 1

    return partitions


if __name__ == "__main__":
    s = "ababcbacadefegdehijhklij"

    result = partition_labels(s)

    print("Partition sizes:", result)
