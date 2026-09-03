class Solution:
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
