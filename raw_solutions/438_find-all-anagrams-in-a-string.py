from collections import Counter

class Solution:
    def findAnagrams(self, s: str, p: str) -> list[int]:
        need = Counter(p)
        window = Counter()
        result = []
        for i, ch in enumerate(s):
            window[ch] += 1
            if i >= len(p):
                left_ch = s[i - len(p)]
                window[left_ch] -= 1
                if window[left_ch] == 0:
                    del window[left_ch]
            if window == need:
                result.append(i - len(p) + 1)
        return result
