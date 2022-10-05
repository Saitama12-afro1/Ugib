class Solution:
    def climbStairs(self, n):
        def fib(n):
            if n <= 1:
                return n
            return fib(n-1) + fib(n-2)
        return fib(n + 1)

n = 4
print(Solution.climbStairs(None, n))
arr = [1,1,1,1,1]
arr_1 = [2,1,1,1]# 2111 1211 1121 1112
arr_3 = [2,2,1]# 221 212 122

arr = arr[1:]
# arr.append(2)