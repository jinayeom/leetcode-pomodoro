class Solution:
    def subsets(self, nums: list[int]) -> list[list[int]]:
        result = [[]]
        for num in nums:
            result += [subset + [num] for subset in result]
        return result
