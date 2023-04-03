class Solution:
    def canPlaceFlowers(self, flowerbed: list[int], n: int) -> bool:
        copy_flowerbed = flowerbed
        for i in range(2,len(copy_flowerbed)):
            if copy_flowerbed[i] == 0:
                if copy_flowerbed[i - 1] == 0 and copy_flowerbed[i+1] == 0:
                    copy_flowerbed[i] = 1
                    n -= 1
        print(copy_flowerbed)
        return True if n == 0 else False

flowerbed = [1,0,0,0,0,1]
n = 2
print(Solution().canPlaceFlowers(flowerbed,n))
            