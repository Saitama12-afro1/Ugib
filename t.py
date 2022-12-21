class Solution:
    def maxNonOverlapping(self,nums: list[int], target:int) -> int:
        answer = []
        last_ind = []
        first_index = []
        for i,val in enumerate(nums):
            if i in last_ind:
                continue
            sum_ = 0
            buff = []
            j = i
            while j < len(nums):
                sum_ += nums[j]
                buff.append(nums[j])
                if sum_ == target:
                    answer.append(buff)
                    last_ind.append([i,j])
                    break
                j += 1 
        last_ind.sort(key = lambda x: x[1])
        count = 0
        for i, val in enumerate(last_ind):
            try:
                if max(val[0], last_ind[i+1][0]) == last_ind[i+1][0] and max(val[1], last_ind[i+1][1]) == last_ind[i+1][1]:
                    count += 1
            except IndexError:
                break
        return count
nums = [-1,3,5,1,4,2,-9]
target = 6

print(Solution.maxNonOverlapping(None, nums, target))
            
                    

