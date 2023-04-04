def findMinDepth(root):
    if root is None:
        return 0
 

    l = findMinDepth(root.left)
 

    r = findMinDepth(root.right)

    if root.left is None:
        return 1 + r
 

    if root.right is None:
        return 1 + l

    return min(l, r) + 1