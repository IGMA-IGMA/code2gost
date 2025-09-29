from flask import Flask, request, send_file, jsonify
from parser.python_parser import PythonParser
from parser.cpp_parser import CppParser
from parser.go_parser import GoParser
from renderer.graph_renderer import render_graph
import io

app = Flask(__name__)

PARSERS = {
    "python": PythonParser(),
    "cpp": CppParser(),
    "go": GoParser(),
}

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json or {}
    lang = (data.get('lang') or '').lower()
    code = data.get('code')
    if not lang or not code:
        return jsonify({"error": "fields 'lang' and 'code' required"}), 400

    parser = PARSERS.get(lang)
    if parser is None:
        return jsonify({"error": f"language '{lang}' not supported"}), 400

    try:
        nodes, edges = parser.parse(code)
    except Exception as e:
        return jsonify({"error": f"parsing failed: {str(e)}"}), 500

    svg_bytes = render_graph(nodes, edges, format='svg')
    return send_file(io.BytesIO(svg_bytes), mimetype='image/svg+xml')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
