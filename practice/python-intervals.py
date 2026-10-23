"""
Python Interval Problems
DSA Practice

Problems:
1. Merge Overlapping Intervals
2. Insert an Interval
3. Check Whether Two Intervals Overlap
4. Find the Minimum Number of Meeting Rooms

Intervals use the format: (start, end)
"""

import heapq


def merge_intervals(intervals):
    """Merge overlapping intervals."""

    if not intervals:
        return []

    intervals = sorted(intervals)
    merged = [list(intervals[0])]

    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])

    return [tuple(interval) for interval in merged]


def insert_interval(intervals, new_interval):
    """Insert an interval into sorted, non-overlapping intervals."""

    result = []
    start, end = new_interval
    index = 0

    while index < len(intervals) and intervals[index][1] < start:
        result.append(intervals[index])
        index += 1

    while index < len(intervals) and intervals[index][0] <= end:
        start = min(start, intervals[index][0])
        end = max(end, intervals[index][1])
        index += 1

    result.append((start, end))
    result.extend(intervals[index:])

    return result


def intervals_overlap(first, second):
    """Check whether two intervals overlap."""

    return max(first[0], second[0]) < min(first[1], second[1])


def minimum_meeting_rooms(intervals):
    """Find the minimum rooms needed for all meetings."""

    if not intervals:
        return 0

    intervals = sorted(intervals)
    active_rooms = []

    for start, end in intervals:
        # A room is available when its meeting ends
        # at or before the next meeting starts.
        if active_rooms and active_rooms[0] <= start:
            heapq.heappop(active_rooms)

        heapq.heappush(active_rooms, end)

    return len(active_rooms)


# --------------------------------------------------
# Example Usage
# --------------------------------------------------

if __name__ == "__main__":

    # 1. Merge Overlapping Intervals
    intervals = [(1, 3), (2, 6), (8, 10), (9, 12)]

    print("Original intervals:", intervals)
    print("Merged intervals:", merge_intervals(intervals))

    # 2. Insert an Interval
    existing = [(1, 2), (5, 7), (8, 10)]
    new_interval = (3, 6)

    print("\nBefore insertion:", existing)
    print("After insertion:", insert_interval(existing, new_interval))

    # 3. Check Overlap
    print(
        "\nDo (1, 5) and (4, 8) overlap?",
        intervals_overlap((1, 5), (4, 8))
    )

    # 4. Minimum Meeting Rooms
    meetings = [(0, 30), (5, 10), (15, 20)]

    print(
        "Minimum meeting rooms:",
        minimum_meeting_rooms(meetings)
    )
