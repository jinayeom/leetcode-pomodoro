class Solution:
    def myAtoi(self, s: str) -> int:
        s = s.lstrip()
        if not s:
            return 0
        sign = 1
        i = 0
        if s[0] in '+-':
            sign = -1 if s[0] == '-' else 1
            i = 1
        digits = ''
        while i < len(s) and s[i].isdigit():
            digits += s[i]
            i += 1
        if not digits:
            return 0
        value = sign * int(digits)
        return max(-2 ** 31, min(2 ** 31 - 1, value))
