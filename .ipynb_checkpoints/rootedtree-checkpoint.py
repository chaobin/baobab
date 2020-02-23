from collections import deque


__all__ = ['RootedTree']


class Node(object):

    def __init__(self, id_, attrs=None):
        self.id_ = id_
        self.inlets = set(())
        self.outlets = set(())
        self.attrs = attrs

    def __eq__(self, other):
        return self.id_ == other.id_

    def __hash__(self):
        return hash(self.id_)

    def is_leaf(self):
        return len(self.outlets) == 0

    def add_inlet(self, node):
        self.inlets.add(node)

    def add_outlet(self, node):
        self.outlets.add(node)

class RootedTree(object):
    
    @classmethod
    def from_records(cls, records):
        g = cls()
        for record in records:
            s_in, s_out = record
            n_in, in_created   = g.create_node(s_in, attrs={}, error=False)
            n_out, out_created = g.create_node(s_out, attrs={}, error=False)
            g.connect(n_in, n_out)    
    
    def __init__(self):
        self._nodes = {}

    def connect(self, p, c):
        # validation
        valid = True
        err = None
        
        
    def traverse(self, node, breadth_first=True):
        queue = deque()
        queue.append(node)
        while queue:
            current = queue.popleft()
            yield current # pre-visit
            if not current.is_leaf():
                if breadth_first:
                    queue.extend(current.outlets)
                else:
                    queue.extendleft(current.outlets)
    
    def get_node(self, id_):
        return self._nodes.get(id_)
    
    def create_node(self, id_, attrs=None, error=True):
        node = self.get_node(id_)
        created = False
        if not node is None:
            if error:
                raise ValueError(f'node with id#{id} already exists')
            else:
                return (node, created)
        node = Node(id_, attrs=attrs)
        created = True
        self._nodes[id_] = node
        return (node, created)