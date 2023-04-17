def max_sequence(arr):
 
    max_so_far = float("-inf")
    max_ending_here = 0
 
    for i in range(0, len(arr)):
        max_ending_here = max_ending_here + arr[i]
        if (max_so_far < max_ending_here):
            max_so_far = max_ending_here
 
        if max_ending_here < 0:
            max_ending_here = 0
    return max_so_far
print(max_sequence([-2, 1, -3, 4, -1, 2, 1, -5, 4]))