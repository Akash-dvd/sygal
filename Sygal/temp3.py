from collections import defaultdict
class Solution:
    def findDuplicateSubtrees(self, root: TreeNode) -> List[TreeNode]:
        self.visited = defaultdict(int)
        ans = []
        self.helper(root, ans)
        return ans
    
    def helper(self, root, ans):
        if not root:
            return '#'.encode()
        res = hash(str(root.val).encode() + self.helper(root.left, ans) + self.helper(root.right, ans))
        res = str(res).encode()
        if self.visited[res] == 1:
            ans.append(root)
        self.visited[res] += 1
        return res
