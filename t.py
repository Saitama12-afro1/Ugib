from copy import deepcopy, copy

some_list = [[1],2,3,4]

some_copy = copy(some_list)
some_deepcopy = deepcopy(some_list)

some_list[0][0] = 10
print(some_list, some_copy, some_deepcopy)