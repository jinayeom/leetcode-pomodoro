#!/usr/bin/env python3
"""
Builds the raw_solutions/*.py scaffold and solutions.json database for Pomodoro Focus.

Usage:
    python3 generate_solutions.py

Add or edit entries in PROBLEMS below, or drop new files straight into raw_solutions/
named "<id>_<slug>.py" and re-run — the JSON is always rebuilt from raw_solutions/.
"""
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(ROOT, "raw_solutions")
OUT_FILE = os.path.join(ROOT, "solutions.json")

# Grind 75 (default order) — id, title, difficulty, and a working Python solution.
PROBLEMS = [
    (1, "Two Sum", "Easy", """class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        seen = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i
        return []
"""),
    (20, "Valid Parentheses", "Easy", """class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        pairs = {')': '(', ']': '[', '}': '{'}
        for ch in s:
            if ch in pairs:
                if not stack or stack.pop() != pairs[ch]:
                    return False
            else:
                stack.append(ch)
        return not stack
"""),
    (21, "Merge Two Sorted Lists", "Easy", """class Solution:
    def mergeTwoLists(self, l1, l2):
        dummy = tail = ListNode()
        while l1 and l2:
            if l1.val <= l2.val:
                tail.next, l1 = l1, l1.next
            else:
                tail.next, l2 = l2, l2.next
            tail = tail.next
        tail.next = l1 or l2
        return dummy.next
"""),
    (121, "Best Time to Buy and Sell Stock", "Easy", """class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        min_price = float('inf')
        best = 0
        for price in prices:
            min_price = min(min_price, price)
            best = max(best, price - min_price)
        return best
"""),
    (125, "Valid Palindrome", "Easy", """class Solution:
    def isPalindrome(self, s: str) -> bool:
        left, right = 0, len(s) - 1
        while left < right:
            while left < right and not s[left].isalnum():
                left += 1
            while left < right and not s[right].isalnum():
                right -= 1
            if s[left].lower() != s[right].lower():
                return False
            left, right = left + 1, right - 1
        return True
"""),
    (226, "Invert Binary Tree", "Easy", """class Solution:
    def invertTree(self, root):
        if not root:
            return None
        root.left, root.right = (
            self.invertTree(root.right),
            self.invertTree(root.left),
        )
        return root
"""),
    (242, "Valid Anagram", "Easy", """from collections import Counter

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        return Counter(s) == Counter(t)
"""),
    (704, "Binary Search", "Easy", """class Solution:
    def search(self, nums: list[int], target: int) -> int:
        lo, hi = 0, len(nums) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                return mid
            if nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return -1
"""),
    (733, "Flood Fill", "Easy", """class Solution:
    def floodFill(self, image, sr, sc, color):
        start = image[sr][sc]
        if start == color:
            return image
        rows, cols = len(image), len(image[0])

        def dfs(r, c):
            if 0 <= r < rows and 0 <= c < cols and image[r][c] == start:
                image[r][c] = color
                dfs(r + 1, c); dfs(r - 1, c)
                dfs(r, c + 1); dfs(r, c - 1)

        dfs(sr, sc)
        return image
"""),
    (235, "Lowest Common Ancestor of a Binary Search Tree", "Easy", """class Solution:
    def lowestCommonAncestor(self, root, p, q):
        node = root
        while node:
            if p.val < node.val and q.val < node.val:
                node = node.left
            elif p.val > node.val and q.val > node.val:
                node = node.right
            else:
                return node
"""),
    (110, "Balanced Binary Tree", "Easy", """class Solution:
    def isBalanced(self, root) -> bool:
        def height(node):
            if not node:
                return 0
            lh = height(node.left)
            rh = height(node.right)
            if lh == -1 or rh == -1 or abs(lh - rh) > 1:
                return -1
            return 1 + max(lh, rh)
        return height(root) != -1
"""),
    (141, "Linked List Cycle", "Easy", """class Solution:
    def hasCycle(self, head) -> bool:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                return True
        return False
"""),
    (232, "Implement Queue using Stacks", "Easy", """class MyQueue:
    def __init__(self):
        self.in_stack = []
        self.out_stack = []

    def push(self, x: int) -> None:
        self.in_stack.append(x)

    def pop(self) -> int:
        self.peek()
        return self.out_stack.pop()

    def peek(self) -> int:
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())
        return self.out_stack[-1]

    def empty(self) -> bool:
        return not self.in_stack and not self.out_stack
"""),
    (278, "First Bad Version", "Easy", """class Solution:
    def firstBadVersion(self, n: int) -> int:
        lo, hi = 1, n
        while lo < hi:
            mid = (lo + hi) // 2
            if isBadVersion(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo
"""),
    (383, "Ransom Note", "Easy", """from collections import Counter

class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        return not (Counter(ransomNote) - Counter(magazine))
"""),
    (70, "Climbing Stairs", "Easy", """class Solution:
    def climbStairs(self, n: int) -> int:
        a, b = 1, 1
        for _ in range(n - 1):
            a, b = b, a + b
        return b
"""),
    (409, "Longest Palindrome", "Easy", """from collections import Counter

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
"""),
    (206, "Reverse Linked List", "Easy", """class Solution:
    def reverseList(self, head):
        prev = None
        while head:
            head.next, prev, head = prev, head, head.next
        return prev
"""),
    (169, "Majority Element", "Easy", """class Solution:
    def majorityElement(self, nums: list[int]) -> int:
        count, candidate = 0, None
        for num in nums:
            if count == 0:
                candidate = num
            count += 1 if num == candidate else -1
        return candidate
"""),
    (67, "Add Binary", "Easy", """class Solution:
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
"""),
    (543, "Diameter of Binary Tree", "Easy", """class Solution:
    def diameterOfBinaryTree(self, root) -> int:
        best = 0

        def depth(node):
            nonlocal best
            if not node:
                return 0
            left = depth(node.left)
            right = depth(node.right)
            best = max(best, left + right)
            return 1 + max(left, right)

        depth(root)
        return best
"""),
    (876, "Middle of the Linked List", "Easy", """class Solution:
    def middleNode(self, head):
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow
"""),
    (104, "Maximum Depth of Binary Tree", "Easy", """class Solution:
    def maxDepth(self, root) -> int:
        if not root:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))
"""),
    (217, "Contains Duplicate", "Easy", """class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        return len(set(nums)) != len(nums)
"""),
    (53, "Maximum Subarray", "Medium", """class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        best = cur = nums[0]
        for num in nums[1:]:
            cur = max(num, cur + num)
            best = max(best, cur)
        return best
"""),
    (57, "Insert Interval", "Medium", """class Solution:
    def insert(self, intervals: list[list[int]], newInterval: list[int]) -> list[list[int]]:
        result = []
        i, n = 0, len(intervals)
        while i < n and intervals[i][1] < newInterval[0]:
            result.append(intervals[i])
            i += 1
        while i < n and intervals[i][0] <= newInterval[1]:
            newInterval[0] = min(newInterval[0], intervals[i][0])
            newInterval[1] = max(newInterval[1], intervals[i][1])
            i += 1
        result.append(newInterval)
        result.extend(intervals[i:])
        return result
"""),
    (542, "01 Matrix", "Medium", """from collections import deque

class Solution:
    def updateMatrix(self, mat: list[list[int]]) -> list[list[int]]:
        rows, cols = len(mat), len(mat[0])
        dist = [[-1] * cols for _ in range(rows)]
        queue = deque()
        for r in range(rows):
            for c in range(cols):
                if mat[r][c] == 0:
                    dist[r][c] = 0
                    queue.append((r, c))

        while queue:
            r, c = queue.popleft()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and dist[nr][nc] == -1:
                    dist[nr][nc] = dist[r][c] + 1
                    queue.append((nr, nc))
        return dist
"""),
    (973, "K Closest Points to Origin", "Medium", """import heapq

class Solution:
    def kClosest(self, points: list[list[int]], k: int) -> list[list[int]]:
        return heapq.nsmallest(k, points, key=lambda p: p[0] ** 2 + p[1] ** 2)
"""),
    (3, "Longest Substring Without Repeating Characters", "Medium", """class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        last_seen = {}
        start = best = 0
        for i, ch in enumerate(s):
            if ch in last_seen and last_seen[ch] >= start:
                start = last_seen[ch] + 1
            last_seen[ch] = i
            best = max(best, i - start + 1)
        return best
"""),
    (15, "3Sum", "Medium", """class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        result = []
        for i in range(len(nums) - 2):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            lo, hi = i + 1, len(nums) - 1
            while lo < hi:
                total = nums[i] + nums[lo] + nums[hi]
                if total < 0:
                    lo += 1
                elif total > 0:
                    hi -= 1
                else:
                    result.append([nums[i], nums[lo], nums[hi]])
                    lo += 1
                    hi -= 1
                    while lo < hi and nums[lo] == nums[lo - 1]:
                        lo += 1
                    while lo < hi and nums[hi] == nums[hi + 1]:
                        hi -= 1
        return result
"""),
    (102, "Binary Tree Level Order Traversal", "Medium", """from collections import deque

class Solution:
    def levelOrder(self, root) -> list[list[int]]:
        if not root:
            return []
        result, queue = [], deque([root])
        while queue:
            level = []
            for _ in range(len(queue)):
                node = queue.popleft()
                level.append(node.val)
                if node.left: queue.append(node.left)
                if node.right: queue.append(node.right)
            result.append(level)
        return result
"""),
    (133, "Clone Graph", "Medium", """class Solution:
    def cloneGraph(self, node):
        if not node:
            return None
        clones = {}

        def dfs(n):
            if n in clones:
                return clones[n]
            copy = Node(n.val)
            clones[n] = copy
            for neighbor in n.neighbors:
                copy.neighbors.append(dfs(neighbor))
            return copy

        return dfs(node)
"""),
    (150, "Evaluate Reverse Polish Notation", "Medium", """class Solution:
    def evalRPN(self, tokens: list[str]) -> int:
        stack = []
        ops = {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: int(a / b),
        }
        for token in tokens:
            if token in ops:
                b, a = stack.pop(), stack.pop()
                stack.append(ops[token](a, b))
            else:
                stack.append(int(token))
        return stack[0]
"""),
    (207, "Course Schedule", "Medium", """from collections import deque

class Solution:
    def canFinish(self, numCourses: int, prerequisites: list[list[int]]) -> bool:
        graph = [[] for _ in range(numCourses)]
        indegree = [0] * numCourses
        for course, pre in prerequisites:
            graph[pre].append(course)
            indegree[course] += 1

        queue = deque(c for c in range(numCourses) if indegree[c] == 0)
        visited = 0
        while queue:
            course = queue.popleft()
            visited += 1
            for nxt in graph[course]:
                indegree[nxt] -= 1
                if indegree[nxt] == 0:
                    queue.append(nxt)
        return visited == numCourses
"""),
    (208, "Implement Trie (Prefix Tree)", "Medium", """class Trie:
    def __init__(self):
        self.children = {}
        self.is_word = False

    def insert(self, word: str) -> None:
        node = self
        for ch in word:
            node = node.children.setdefault(ch, Trie())
        node.is_word = True

    def _find(self, word: str):
        node = self
        for ch in word:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def search(self, word: str) -> bool:
        node = self._find(word)
        return node is not None and node.is_word

    def startsWith(self, prefix: str) -> bool:
        return self._find(prefix) is not None
"""),
    (322, "Coin Change", "Medium", """class Solution:
    def coinChange(self, coins: list[int], amount: int) -> int:
        dp = [0] + [float('inf')] * amount
        for a in range(1, amount + 1):
            for coin in coins:
                if coin <= a:
                    dp[a] = min(dp[a], dp[a - coin] + 1)
        return dp[amount] if dp[amount] != float('inf') else -1
"""),
    (238, "Product of Array Except Self", "Medium", """class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        n = len(nums)
        result = [1] * n
        prefix = 1
        for i in range(n):
            result[i] = prefix
            prefix *= nums[i]
        suffix = 1
        for i in range(n - 1, -1, -1):
            result[i] *= suffix
            suffix *= nums[i]
        return result
"""),
    (155, "Min Stack", "Medium", """class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        m = val if not self.min_stack else min(val, self.min_stack[-1])
        self.min_stack.append(m)

    def pop(self) -> None:
        self.stack.pop()
        self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]
"""),
    (98, "Validate Binary Search Tree", "Medium", """class Solution:
    def isValidBST(self, root) -> bool:
        def valid(node, lo, hi):
            if not node:
                return True
            if not (lo < node.val < hi):
                return False
            return valid(node.left, lo, node.val) and valid(node.right, node.val, hi)

        return valid(root, float('-inf'), float('inf'))
"""),
    (200, "Number of Islands", "Medium", """class Solution:
    def numIslands(self, grid: list[list[str]]) -> int:
        rows, cols = len(grid), len(grid[0])

        def sink(r, c):
            if 0 <= r < rows and 0 <= c < cols and grid[r][c] == '1':
                grid[r][c] = '0'
                sink(r + 1, c); sink(r - 1, c)
                sink(r, c + 1); sink(r, c - 1)

        count = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '1':
                    count += 1
                    sink(r, c)
        return count
"""),
    (994, "Rotting Oranges", "Medium", """from collections import deque

class Solution:
    def orangesRotting(self, grid: list[list[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        queue = deque()
        fresh = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 2:
                    queue.append((r, c, 0))
                elif grid[r][c] == 1:
                    fresh += 1

        minutes = 0
        while queue:
            r, c, minutes = queue.popleft()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    queue.append((nr, nc, minutes + 1))
        return minutes if fresh == 0 else -1
"""),
    (33, "Search in Rotated Sorted Array", "Medium", """class Solution:
    def search(self, nums: list[int], target: int) -> int:
        lo, hi = 0, len(nums) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                return mid
            if nums[lo] <= nums[mid]:
                if nums[lo] <= target < nums[mid]:
                    hi = mid - 1
                else:
                    lo = mid + 1
            else:
                if nums[mid] < target <= nums[hi]:
                    lo = mid + 1
                else:
                    hi = mid - 1
        return -1
"""),
    (39, "Combination Sum", "Medium", """class Solution:
    def combinationSum(self, candidates: list[int], target: int) -> list[list[int]]:
        result = []

        def backtrack(start, remaining, path):
            if remaining == 0:
                result.append(path[:])
                return
            for i in range(start, len(candidates)):
                if candidates[i] > remaining:
                    continue
                path.append(candidates[i])
                backtrack(i, remaining - candidates[i], path)
                path.pop()

        backtrack(0, target, [])
        return result
"""),
    (46, "Permutations", "Medium", """class Solution:
    def permute(self, nums: list[int]) -> list[list[int]]:
        result = []

        def backtrack(path, remaining):
            if not remaining:
                result.append(path[:])
                return
            for i in range(len(remaining)):
                path.append(remaining[i])
                backtrack(path, remaining[:i] + remaining[i + 1:])
                path.pop()

        backtrack([], nums)
        return result
"""),
    (56, "Merge Intervals", "Medium", """class Solution:
    def merge(self, intervals: list[list[int]]) -> list[list[int]]:
        intervals.sort(key=lambda iv: iv[0])
        merged = []
        for start, end in intervals:
            if merged and start <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], end)
            else:
                merged.append([start, end])
        return merged
"""),
    (236, "Lowest Common Ancestor of a Binary Tree", "Medium", """class Solution:
    def lowestCommonAncestor(self, root, p, q):
        if not root or root == p or root == q:
            return root
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        if left and right:
            return root
        return left or right
"""),
    (981, "Time Based Key-Value Store", "Medium", """from collections import defaultdict
import bisect

class TimeMap:
    def __init__(self):
        self.store = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.store[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        entries = self.store.get(key, [])
        i = bisect.bisect_right(entries, (timestamp, chr(0x10FFFF)))
        return entries[i - 1][1] if i else ""
"""),
    (721, "Accounts Merge", "Medium", """class Solution:
    def accountsMerge(self, accounts: list[list[str]]) -> list[list[str]]:
        parent = list(range(len(accounts)))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

        email_to_acct = {}
        for i, account in enumerate(accounts):
            for email in account[1:]:
                if email in email_to_acct:
                    union(i, email_to_acct[email])
                else:
                    email_to_acct[email] = i

        groups = {}
        for email, i in email_to_acct.items():
            root = find(i)
            groups.setdefault(root, set()).add(email)

        result = []
        for i, emails in groups.items():
            result.append([accounts[i][0]] + sorted(emails))
        return result
"""),
    (75, "Sort Colors", "Medium", """class Solution:
    def sortColors(self, nums: list[int]) -> None:
        low, mid, high = 0, 0, len(nums) - 1
        while mid <= high:
            if nums[mid] == 0:
                nums[low], nums[mid] = nums[mid], nums[low]
                low += 1
                mid += 1
            elif nums[mid] == 1:
                mid += 1
            else:
                nums[mid], nums[high] = nums[high], nums[mid]
                high -= 1
"""),
    (139, "Word Break", "Medium", """class Solution:
    def wordBreak(self, s: str, wordDict: list[str]) -> bool:
        words = set(wordDict)
        dp = [False] * (len(s) + 1)
        dp[0] = True
        for i in range(1, len(s) + 1):
            for j in range(i):
                if dp[j] and s[j:i] in words:
                    dp[i] = True
                    break
        return dp[-1]
"""),
    (416, "Partition Equal Subset Sum", "Medium", """class Solution:
    def canPartition(self, nums: list[int]) -> bool:
        total = sum(nums)
        if total % 2:
            return False
        target = total // 2
        dp = [False] * (target + 1)
        dp[0] = True
        for num in nums:
            for t in range(target, num - 1, -1):
                dp[t] = dp[t] or dp[t - num]
        return dp[target]
"""),
    (8, "String to Integer (atoi)", "Medium", """class Solution:
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
"""),
    (54, "Spiral Matrix", "Medium", """class Solution:
    def spiralOrder(self, matrix: list[list[int]]) -> list[int]:
        result = []
        top, bottom = 0, len(matrix) - 1
        left, right = 0, len(matrix[0]) - 1
        while top <= bottom and left <= right:
            for c in range(left, right + 1):
                result.append(matrix[top][c])
            top += 1
            for r in range(top, bottom + 1):
                result.append(matrix[r][right])
            right -= 1
            if top <= bottom:
                for c in range(right, left - 1, -1):
                    result.append(matrix[bottom][c])
                bottom -= 1
            if left <= right:
                for r in range(bottom, top - 1, -1):
                    result.append(matrix[r][left])
                left += 1
        return result
"""),
    (78, "Subsets", "Medium", """class Solution:
    def subsets(self, nums: list[int]) -> list[list[int]]:
        result = [[]]
        for num in nums:
            result += [subset + [num] for subset in result]
        return result
"""),
    (199, "Binary Tree Right Side View", "Medium", """from collections import deque

class Solution:
    def rightSideView(self, root) -> list[int]:
        if not root:
            return []
        result, queue = [], deque([root])
        while queue:
            level_size = len(queue)
            for i in range(level_size):
                node = queue.popleft()
                if i == level_size - 1:
                    result.append(node.val)
                if node.left: queue.append(node.left)
                if node.right: queue.append(node.right)
        return result
"""),
    (5, "Longest Palindromic Substring", "Medium", """class Solution:
    def longestPalindrome(self, s: str) -> str:
        if not s:
            return ""
        start, end = 0, 0

        def expand(l, r):
            while l >= 0 and r < len(s) and s[l] == s[r]:
                l -= 1
                r += 1
            return l + 1, r - 1

        for i in range(len(s)):
            l1, r1 = expand(i, i)
            if r1 - l1 > end - start:
                start, end = l1, r1
            l2, r2 = expand(i, i + 1)
            if r2 - l2 > end - start:
                start, end = l2, r2
        return s[start:end + 1]
"""),
    (62, "Unique Paths", "Medium", """class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        dp = [1] * n
        for _ in range(1, m):
            for j in range(1, n):
                dp[j] += dp[j - 1]
        return dp[-1]
"""),
    (105, "Construct Binary Tree from Preorder and Inorder Traversal", "Medium", """class Solution:
    def buildTree(self, preorder: list[int], inorder: list[int]):
        index = {val: i for i, val in enumerate(inorder)}
        self.pre_idx = 0

        def build(left, right):
            if left > right:
                return None
            val = preorder[self.pre_idx]
            self.pre_idx += 1
            node = TreeNode(val)
            mid = index[val]
            node.left = build(left, mid - 1)
            node.right = build(mid + 1, right)
            return node

        return build(0, len(inorder) - 1)
"""),
    (11, "Container With Most Water", "Medium", """class Solution:
    def maxArea(self, height: list[int]) -> int:
        left, right = 0, len(height) - 1
        best = 0
        while left < right:
            best = max(best, (right - left) * min(height[left], height[right]))
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
        return best
"""),
    (17, "Letter Combinations of a Phone Number", "Medium", """class Solution:
    def letterCombinations(self, digits: str) -> list[str]:
        if not digits:
            return []
        mapping = {
            '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
            '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
        }
        result = ['']
        for digit in digits:
            result = [prefix + ch for prefix in result for ch in mapping[digit]]
        return result
"""),
    (79, "Word Search", "Medium", """class Solution:
    def exist(self, board: list[list[str]], word: str) -> bool:
        rows, cols = len(board), len(board[0])

        def dfs(r, c, i):
            if i == len(word):
                return True
            if not (0 <= r < rows and 0 <= c < cols) or board[r][c] != word[i]:
                return False
            temp, board[r][c] = board[r][c], '#'
            found = (dfs(r + 1, c, i + 1) or dfs(r - 1, c, i + 1) or
                     dfs(r, c + 1, i + 1) or dfs(r, c - 1, i + 1))
            board[r][c] = temp
            return found

        return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))
"""),
    (438, "Find All Anagrams in a String", "Medium", """from collections import Counter

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
"""),
    (310, "Minimum Height Trees", "Medium", """from collections import deque

class Solution:
    def findMinHeightTrees(self, n: int, edges: list[list[int]]) -> list[int]:
        if n == 1:
            return [0]
        graph = [set() for _ in range(n)]
        for a, b in edges:
            graph[a].add(b)
            graph[b].add(a)

        leaves = deque(i for i in range(n) if len(graph[i]) == 1)
        remaining = n
        while remaining > 2:
            leaf_count = len(leaves)
            remaining -= leaf_count
            for _ in range(leaf_count):
                leaf = leaves.popleft()
                neighbor = graph[leaf].pop()
                graph[neighbor].discard(leaf)
                if len(graph[neighbor]) == 1:
                    leaves.append(neighbor)
        return list(leaves)
"""),
    (621, "Task Scheduler", "Medium", """from collections import Counter

class Solution:
    def leastInterval(self, tasks: list[str], n: int) -> int:
        counts = Counter(tasks)
        max_count = max(counts.values())
        max_count_tasks = sum(1 for c in counts.values() if c == max_count)
        return max(len(tasks), (max_count - 1) * (n + 1) + max_count_tasks)
"""),
    (146, "LRU Cache", "Medium", """from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
"""),
    (230, "Kth Smallest Element in a BST", "Medium", """class Solution:
    def kthSmallest(self, root, k: int) -> int:
        stack = []
        node = root
        while stack or node:
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()
            k -= 1
            if k == 0:
                return node.val
            node = node.right
"""),
    (76, "Minimum Window Substring", "Hard", """from collections import Counter

class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if not s or not t:
            return ""
        need = Counter(t)
        missing = len(t)
        left = start = end = 0
        for right, ch in enumerate(s, 1):
            if need[ch] > 0:
                missing -= 1
            need[ch] -= 1
            if missing == 0:
                while need[s[left]] < 0:
                    need[s[left]] += 1
                    left += 1
                if end == 0 or right - left < end - start:
                    start, end = left, right
                need[s[left]] += 1
                missing += 1
                left += 1
        return s[start:end]
"""),
    (297, "Serialize and Deserialize Binary Tree", "Hard", """class Codec:
    def serialize(self, root) -> str:
        vals = []

        def dfs(node):
            if not node:
                vals.append('#')
                return
            vals.append(str(node.val))
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return ','.join(vals)

    def deserialize(self, data: str):
        vals = iter(data.split(','))

        def build():
            val = next(vals)
            if val == '#':
                return None
            node = TreeNode(int(val))
            node.left = build()
            node.right = build()
            return node

        return build()
"""),
    (42, "Trapping Rain Water", "Hard", """class Solution:
    def trap(self, height: list[int]) -> int:
        if not height:
            return 0
        left, right = 0, len(height) - 1
        left_max, right_max = height[left], height[right]
        water = 0
        while left < right:
            if left_max < right_max:
                left += 1
                left_max = max(left_max, height[left])
                water += left_max - height[left]
            else:
                right -= 1
                right_max = max(right_max, height[right])
                water += right_max - height[right]
        return water
"""),
    (295, "Find Median from Data Stream", "Hard", """import heapq

class MedianFinder:
    def __init__(self):
        self.small = []  # max-heap (negated)
        self.large = []  # min-heap

    def addNum(self, num: int) -> None:
        heapq.heappush(self.small, -num)
        heapq.heappush(self.large, -heapq.heappop(self.small))
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2
"""),
    (127, "Word Ladder", "Hard", """from collections import deque

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: list[str]) -> int:
        words = set(wordList)
        if endWord not in words:
            return 0
        queue = deque([(beginWord, 1)])
        while queue:
            word, steps = queue.popleft()
            if word == endWord:
                return steps
            for i in range(len(word)):
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    candidate = word[:i] + c + word[i + 1:]
                    if candidate in words:
                        words.remove(candidate)
                        queue.append((candidate, steps + 1))
        return 0
"""),
    (224, "Basic Calculator", "Hard", """class Solution:
    def calculate(self, s: str) -> int:
        stack = []
        result = 0
        number = 0
        sign = 1
        for ch in s:
            if ch.isdigit():
                number = number * 10 + int(ch)
            elif ch in '+-':
                result += sign * number
                number = 0
                sign = 1 if ch == '+' else -1
            elif ch == '(':
                stack.append(result)
                stack.append(sign)
                result = 0
                sign = 1
            elif ch == ')':
                result += sign * number
                number = 0
                result *= stack.pop()
                result += stack.pop()
        return result + sign * number
"""),
    (1235, "Maximum Profit in Job Scheduling", "Hard", """import bisect

class Solution:
    def jobScheduling(self, startTime: list[int], endTime: list[int], profit: list[int]) -> int:
        jobs = sorted(zip(startTime, endTime, profit), key=lambda j: j[1])
        ends = [job[1] for job in jobs]
        dp = [0] * (len(jobs) + 1)
        for i, (start, end, prof) in enumerate(jobs):
            j = bisect.bisect_right(ends, start, 0, i)
            dp[i + 1] = max(dp[i], dp[j] + prof)
        return dp[-1]
"""),
    (23, "Merge k Sorted Lists", "Hard", """import heapq

class Solution:
    def mergeKLists(self, lists):
        heap = []
        for i, node in enumerate(lists):
            if node:
                heapq.heappush(heap, (node.val, i, node))

        dummy = tail = ListNode()
        while heap:
            val, i, node = heapq.heappop(heap)
            tail.next = node
            tail = tail.next
            if node.next:
                heapq.heappush(heap, (node.next.val, i, node.next))
        return dummy.next
"""),
    (84, "Largest Rectangle in Histogram", "Hard", """class Solution:
    def largestRectangleArea(self, heights: list[int]) -> int:
        stack = []
        best = 0
        for i, h in enumerate(heights + [0]):
            while stack and heights[stack[-1]] >= h:
                height = heights[stack.pop()]
                width = i if not stack else i - stack[-1] - 1
                best = max(best, height * width)
            stack.append(i)
        return best
"""),
]


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug


def main():
    os.makedirs(RAW_DIR, exist_ok=True)

    # Clear stale files so removed/renamed problems don't linger in raw_solutions/.
    for f in glob.glob(os.path.join(RAW_DIR, "*.py")):
        os.remove(f)

    for pid, title, difficulty, code in PROBLEMS:
        filename = f"{pid}_{slugify(title)}.py"
        with open(os.path.join(RAW_DIR, filename), "w") as f:
            f.write(code.strip() + "\n")

    # Rebuild solutions.json straight from raw_solutions/ so hand-added files work too.
    problems = []
    for path in sorted(
        glob.glob(os.path.join(RAW_DIR, "*.py")),
        key=lambda p: int(os.path.basename(p).split("_", 1)[0])
    ):
        name = os.path.splitext(os.path.basename(path))[0]
        num, _, slug = name.partition("_")
        with open(path) as f:
            code = f.read().rstrip()
        # Look up difficulty/title from PROBLEMS by id (raw_solutions/ only stores the slug).
        meta = next((p for p in PROBLEMS if str(p[0]) == num), None)
        title = meta[1] if meta else slug.replace("-", " ").title()
        difficulty = meta[2] if meta else "Medium"
        problems.append({
            "id": int(num) if num.isdigit() else None,
            "title": title,
            "difficulty": difficulty,
            "solution": code,
        })

    with open(OUT_FILE, "w") as f:
        json.dump(problems, f, indent=2)
        f.write("\n")

    print(f"Wrote {len(problems)} problems to raw_solutions/ and {OUT_FILE}")


if __name__ == "__main__":
    main()
