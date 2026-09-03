from collections import Counter

class Solution:
    def leastInterval(self, tasks: list[str], n: int) -> int:
        counts = Counter(tasks)
        max_count = max(counts.values())
        max_count_tasks = sum(1 for c in counts.values() if c == max_count)
        return max(len(tasks), (max_count - 1) * (n + 1) + max_count_tasks)
