import bisect

class Solution:
    def jobScheduling(self, startTime: list[int], endTime: list[int], profit: list[int]) -> int:
        jobs = sorted(zip(startTime, endTime, profit), key=lambda j: j[1])
        ends = [job[1] for job in jobs]
        dp = [0] * (len(jobs) + 1)
        for i, (start, end, prof) in enumerate(jobs):
            j = bisect.bisect_right(ends, start, 0, i)
            dp[i + 1] = max(dp[i], dp[j] + prof)
        return dp[-1]
