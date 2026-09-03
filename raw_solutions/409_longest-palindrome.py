from collections import Counter

class Solution:
    def longestPalindrome(self, s: str) -> int:
        counts = Counter(s)
        length = 0
        odd_found = False
        for c in counts.values():
            length += c - (c % 2)
            if c % 2:
                odd_found = True
        return length + 1 if odd_found else length
