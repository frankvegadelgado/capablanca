def max_non_overlapping_intervals(intervals):
    # Sort intervals by their end points
    intervals.sort(key=lambda x: x[1])
    
    # Initialize the list of selected intervals
    selected_intervals = []
    
    # Initialize the end point of the last selected interval
    last_end = float('-inf')
    
    # Iterate through the sorted intervals
    for interval in intervals:
        start, end = interval
        # Select the interval if it does not overlap with the last selected interval
        if start > last_end:
            selected_intervals.append(interval)
            last_end = end
    
    return selected_intervals

# Example usage
intervals = [(1, 3), (2, 5), (3, 7), (4, 6), (5, 8)]
selected_intervals = max_non_overlapping_intervals(intervals)
print("Selected intervals:", selected_intervals)
print("Maximum number of non-overlapping intervals:", len(selected_intervals))