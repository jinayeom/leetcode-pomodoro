class Solution:
    def addBinary(self, a: str, b: str) -> str:
        result, carry = [], 0
        a, b = list(a), list(b)
        while a or b or carry:
            total = carry
            if a: total += int(a.pop())
            if b: total += int(b.pop())
            result.append(str(total % 2))
            carry = total // 2
        return ''.join(reversed(result))
