from parser.base_parser import ParserBase
from tree_sitter import Parser, Language
import os

# You may build a shared lib with required grammars (cpp, go, etc.) and set LIB_PATH accordingly
BUILD_DIR = os.path.join(os.path.dirname(__file__), '..', 'build')
LIB_PATH = os.path.join(BUILD_DIR, 'my-languages.so')

CPP_LANG = None
if os.path.exists(LIB_PATH):
    try:
        CPP_LANG = Language(LIB_PATH, 'cpp')
    except Exception:
        CPP_LANG = None

class Node:
    def __init__(self, id, label, type):
        self.id = id; self.label = label; self.type = type
class Edge:
    def __init__(self, from_id, to_id, label=None):
        self.from_id = from_id; self.to_id = to_id; self.label = label

class CppParser(ParserBase):
    def __init__(self):
        self.parser = Parser()
        if CPP_LANG is None:
            raise RuntimeError('C++ language not loaded. Build my-languages.so with tree-sitter-cpp.')
        self.parser.set_language(CPP_LANG)

    def parse(self, code: str):
        tree = self.parser.parse(bytes(code, 'utf8'))
        root = tree.root_node
        nodes = []
        edges = []
        counter = 0
        def next_id():
            nonlocal counter; counter += 1; return f'n{counter}'
        start = next_id(); nodes.append(Node(start, 'Начало', 'StartEnd'))

        def extract(node, prevs):
            nonlocal nodes, edges
            kind = node.type
            if kind == 'if_statement':
                d_id = next_id(); nodes.append(Node(d_id, 'Если ... ?', 'Decision'))
                for pid in prevs: edges.append(Edge(pid, d_id))
                then_prevs = [d_id]
                for child in node.named_children:
                    then_prevs = extract(child, then_prevs)
                after = next_id(); nodes.append(Node(after, '', 'Process'))
                for tp in then_prevs: edges.append(Edge(tp, after, 'да'))
                return [after]
            elif kind == 'return_statement':
                rid = next_id(); nodes.append(Node(rid, node.text.decode('utf8'), 'Process'))
                for pid in prevs: edges.append(Edge(pid, rid))
                return [rid]
            else:
                curr = prevs
                for child in node.named_children:
                    curr = extract(child, curr)
                return curr

        last = extract(root, [start])
        end = next_id(); nodes.append(Node(end, 'Конец', 'StartEnd'))
        for l in last: edges.append(Edge(l, end))
        return nodes, edges
