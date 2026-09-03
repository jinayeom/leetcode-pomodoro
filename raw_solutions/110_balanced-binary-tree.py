class Solution:
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
