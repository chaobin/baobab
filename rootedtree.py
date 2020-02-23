import os
from collections import deque


__all__ = ['RootedTree']


class Node(object):

    def __init__(self, id_, inlet, attrs=None):
        self.id_ = id_
        self.inlet = inlet
        self.outlets = set(())
        self.attrs = attrs or {}

    def __eq__(self, other):
        return self.id_ == other.id_

    def __hash__(self):
        return hash(self.id_)

    def __str__(self):
        return self.attrs.get('name', self.id_)

    def __repr__(self):
        return f'{self.inlet}->{self}'

    def is_leaf(self):
        return len(self.outlets) == 0

    def remove_outlet(self, node):
        if node in self.outlets:
            self.outlets.remove(node)

    def add_outlet(self, node):
        # validation
        if self == node:
            raise ValueError(f'"{self.id_}"" cannot connect to itself "{node.id_}"')
        if node in self.outlets: return
        node.inlet.remove_outlet(node)
        node.inlet = self
        self.outlets.add(node)

class RootedTree(object):
    
    @classmethod
    def from_records(cls, records):
        tree = cls()
        for record in records:
            s_in, s_out = record
            n_in, in_created   = tree.create_node(s_in, attrs={}, error=False)
            n_out, out_created = tree.create_node(s_out, inlet=n_in, attrs={}, error=False)
            n_in.add_outlet(n_out)
        return tree
    
    def __init__(self):
        self._nodes = {}

    def traverse(self, node, depth_first=True):
        queue = deque()
        queue.append((0, node))
        while queue:
            depth, current = queue.popleft()
            yield (depth, current) # pre-visit
            if not current.is_leaf():
                children = [(depth + 1, n) for n in current.outlets]
                if depth_first:
                    queue.extendleft(children)
                else:
                    queue.extend(children)
    
    def get_node(self, id_):
        return self._nodes.get(id_)
    
    def create_node(self, id_, inlet=None, attrs=None, error=True):
        node = self.get_node(id_)
        created = False
        if not node is None:
            if error:
                raise ValueError(f'node with id#{id} already exists')
            else:
                return (node, created)
        node = Node(id_, inlet=inlet, attrs=attrs)
        created = True
        self._nodes[id_] = node
        return (node, created)

    def to_string(self, node):
        lines = []
        for (depth, n) in self.traverse(node):
            s = f'{" " * depth}{"-" if n.is_leaf() else "+"}{n}'
            lines.append(s)
        return lines

    def print_tree(self, node):
        lines = self.to_string(node)
        print(os.linesep.join(lines))

