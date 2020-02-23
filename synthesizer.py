import yaml
import copy

from baobab.rootedtree import Node, RootedTree


class Synthesizer(object):

    @classmethod
    def from_yaml(cls, fname:str):
        with open(fname) as f:
            spec = yaml.load(f, Loader=yaml.FullLoader)
            meta = spec['meta']
            coding = spec['code']
        return cls(coding)

    def __init__(self, coding):
        self.coding = coding

    def synthesize(self, tree:RootedTree) -> RootedTree:
        '''
        One-pass the tree, and synthesize another
        by interpreting the coding.
        '''
        synth = copy.deepcopy(tree)
        for (id_, code) in self.coding.items():
            n_inlet, _ = synth.create_node(code['IN'], error=False)
            node, created = synth.create_node(id_, n_inlet, attrs=code, error=False)
            if not created: node.attrs.update(code)
            n_inlet.add_outlet(node)
        return synth
