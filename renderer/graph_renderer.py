import graphviz
from gost_styles import NODE_STYLES, EDGE_STYLES

def render_graph(nodes, edges, format='svg'):
    dot = graphviz.Digraph(format=format)
    for n in nodes:
        style = NODE_STYLES.get(n.type, {})
        dot.node(n.id, n.label or '', **style)
    for e in edges:
        attrs = EDGE_STYLES.get('default', {})
        if getattr(e, 'label', None):
            dot.edge(e.from_id, e.to_id, label=e.label, **attrs)
        else:
            dot.edge(e.from_id, e.to_id, **attrs)
    return dot.pipe()
