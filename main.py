class BTreeNode:
    def __init__(self, leaf=True): self.leaf, self.keys, self.vals, self.kids = leaf, [], [], []

class BTree:
    def __init__(self, t=2): self.t, self.root = t, BTreeNode(True)
    def search(self, k, node=None):
        node = node or self.root; i = 0
        while i < len(node.keys) and k > node.keys[i]: i += 1
        if i < len(node.keys) and k == node.keys[i]: return node.vals[i]
        return None if node.leaf else self.search(k, node.kids[i])
    def insert(self, k, v):
        r = self.root
        if len(r.keys) == 2*self.t - 1:
            s = BTreeNode(False); self.root = s; s.kids.append(r)
            self._split(s, 0); self._insert_nonfull(s, k, v)
        else: self._insert_nonfull(r, k, v)
    def _split(self, x, i):
        t, y, z = self.t, x.kids[i], BTreeNode(x.kids[i].leaf)
        x.keys.insert(i, y.keys[t-1]); x.vals.insert(i, y.vals[t-1]); x.kids.insert(i+1, z)
        z.keys, z.vals = y.keys[t:], y.vals[t:]; y.keys, y.vals = y.keys[:t-1], y.vals[:t-1]
        if not y.leaf: z.kids, y.kids = y.kids[t:], y.kids[:t]
    def _insert_nonfull(self, x, k, v):
        i = len(x.keys) - 1
        if x.leaf:
            while i >= 0 and k < x.keys[i]: i -= 1
            x.keys.insert(i+1, k); x.vals.insert(i+1, v)
        else:
            while i >= 0 and k < x.keys[i]: i -= 1
            i += 1
            if len(x.kids[i].keys) == 2*self.t - 1:
                self._split(x, i)
                if k > x.keys[i]: i += 1
            self._insert_nonfull(x.kids[i], k, v)

if __name__ == "__main__":
    bt = BTree(2)
    for i in range(25): bt.insert(i*3, f"row_{i}")
    assert bt.search(36) == "row_12" and bt.search(37) is None
    print("[PASS] 010_b_tree_index")
