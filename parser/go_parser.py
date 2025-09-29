from parser.base_parser import ParserBase
from tree_sitter import Parser, Language
import os

BUILD_DIR = os.path.join(os.path.dirname(__file__), '..', 'build')
LIB_PATH = os.path.join(BUILD_DIR, 'my-languages.so')

GO_LANG = None
if os.path.exists(LIB_PATH):
    try:
        GO_LANG = Language(LIB_PATH, 'go')
    except Exception:
        GO_LANG = None

class Node:
    def __init__(self, id, label, type):
        self.id = id; self.label = label; self.type = type
class Edge:
    def __init__(self, from_id, to_id, label=None):
        self.from_id = from_id; self.to_id = to_id; self.label = label

class GoParser(ParserBase):
    def __init__(self):
        self.parser = Parser()
        if GO_LANG is None:
            raise RuntimeError('Go language not loaded. Build my-languages.so with tree-sitter-go.')
        self.parser.set_language(GO_LANG)

    def parse(self, code: str):
        tree = self.parser.parse(bytes(code, 'utf8'))
        root = tree.root_node
        nodes = []
        edges = []
        counter = 0
        def next_id():
            nonlocal counter; counter += 1; return f'n{counter}'
        start = next_id(); nodes.append(Node(start, 'Начало', 'StartEnd'))

        def walk(node, prevs):
            nonlocal nodes, edges
            kind = node.type
            if kind == 'if_statement':
                d = next_id(); nodes.append(Node(d, 'Если ... ?', 'Decision'))
                for p in prevs: edges.append(Edge(p, d))
                then_prevs = [d]
                for child in node.named_children:
                    then_prevs = walk(child, then_prevs)
                after = next_id(); nodes.append(Node(after, '', 'Process'))
                for tp in then_prevs: edges.append(Edge(tp, after, 'да'))
                return [after]
            elif kind == 'for_statement':
                d = next_id(); nodes.append(Node(d, 'for', 'Decision'))
                for p in prevs: edges.append(Edge(p, d))
                body_prevs = [d]
                for child in node.named_children:
                    body_prevs = walk(child, body_prevs)
                for bp in body_prevs: edges.append(Edge(bp, d, label='повтор'))
                after = next_id(); nodes.append(Node(after, '', 'Process'))
                edges.append(Edge(d, after, label='нет'))
                return [after]
            elif kind == 'return_statement':
                nid = next_id(); nodes.append(Node(nid, node.text.decode('utf8'), 'Process'))
                for p in prevs: edges.append(Edge(p, nid))
                return [nid]
            elif kind == 'block':
                curr_prevs = prevs
                for child in node.named_children:
                    curr_prevs = walk(child, curr_prevs)
                return curr_prevs
            else:
                curr = prevs
                for child in node.named_children:
                    curr = walk(child, curr)
                return curr

        last = walk(root, [start])
        end = next_id(); nodes.append(Node(end, 'Конец', 'StartEnd'))
        for l in last: edges.append(Edge(l, end))
        return nodes, edges
