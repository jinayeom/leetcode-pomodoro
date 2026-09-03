class Solution:
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
