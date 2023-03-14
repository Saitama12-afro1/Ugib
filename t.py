class Solution:
    def minimumDifference(self, nums: list[int]) -> int:
        arr_1 = [nums[0]]
        arr_2 = [nums[1]]
        s1 = nums[0]
        s2 = nums[1]
        answer = abs(nums[0] - nums[1])
        for i in range(2, len(nums), 2):
            if  (s1 + nums[i] - (s2 + nums[i+1])) <= (s1 + nums[i+1] - (s2 + nums[i])):
                arr_1.append(nums[i])
                arr_2.append(nums[i+1])
                s1 += nums[i]
                s2 += nums[i+1]
                answer = abs(s1 - s2)
                
            else:
                arr_1.append(nums[i+1])
                arr_2.append(nums[i])
                s1 += nums[i]
                s2 += nums[i+1]
                answer = (s1  - s2)
        print(arr_1, arr_2)
        return answer
            

nums = [2,-1,0,4,-2,-9]
print(Solution().minimumDifference(nums))