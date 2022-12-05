class Solution:
    def levelOrder(self, root, answer = []):
        while True:
            answer.append(root.val)
            answer.append(root.left)
            answer.append(root.right)
            if not root.left and not root.right:
                break
            if root.left.val:            
                self.levelOrder(root = root.left)
            if root.right.val:
                self.levelOrder(root = root.right)
            print(answer)
            
        return answer
    
a = None