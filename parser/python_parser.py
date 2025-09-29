import ast
from parser.base_parser import ParserBase

class Node:
    def __init__(self, id, label, type):
        self.id = id
        self.label = label
        self.type = type

class Edge:
    def __init__(self, from_id, to_id, label=None):
        self.from_id = from_id
        self.to_id = to_id
        self.label = label

class PythonParser(ParserBase):
    def parse(self, code: str):
        tree = ast.parse(code)
        nodes = []
        edges = []
        counter = 0
        def next_id():
            nonlocal counter
            counter += 1
            return f"n{counter}"

        start = next_id(); nodes.append(Node(start, 'Начало', 'StartEnd'))
        prev = start

        def handle(stmt, prev):
            if isinstance(stmt, ast.Assign) or isinstance(stmt, ast.Expr) or isinstance(stmt, ast.Return):
                nid = next_id()
                label = ast.unparse(stmt).strip() if hasattr(ast, 'unparse') else ast.dump(stmt)
                nodes.append(Node(nid, label, 'Process'))
                edges.append(Edge(prev, nid))
                return nid
            elif isinstance(stmt, ast.If):
                d = next_id(); cond = ast.unparse(stmt.test)
                nodes.append(Node(d, f'Если {cond} ?', 'Decision'))
                edges.append(Edge(prev, d))
                then_prev = d
                for s in stmt.body:
                    then_prev = handle(s, then_prev)
                else_prev = d
                for s in stmt.orelse:
                    else_prev = handle(s, else_prev)
                after = next_id(); nodes.append(Node(after, '', 'Process'))
                edges.append(Edge(then_prev, after, 'да'))
                edges.append(Edge(else_prev, after, 'нет'))
                return after
            else:
                nid = next_id(); nodes.append(Node(nid, type(stmt).__name__, 'Process'))
                edges.append(Edge(prev, nid))
                return nid

        last = prev
        for s in tree.body:
            last = handle(s, last)

        end = next_id(); nodes.append(Node(end, 'Конец', 'StartEnd'))
        edges.append(Edge(last, end))

        return nodes, edges
