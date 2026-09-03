class Solution:
    def isValidBST(self, root) -> bool:
        def valid(node, lo, hi):
            if not node:
                return True
            if not (lo < node.val < hi):
                return False
            return valid(node.left, lo, node.val) and valid(node.right, node.val, hi)

        return valid(root, float('-inf'), float('inf'))
