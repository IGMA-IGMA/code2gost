# code2gost
Multi-language code -> ГОСТ block diagrams (prototype)

This repository provides a Python server that parses source code (Python, C++, Go) and
generates block-diagrams (SVG) styled in the spirit of ГОСТ (standard flowchart symbols).

Quick start:
1. Create virtual environment and install requirements:
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
2. Install Graphviz (system package) so `graphviz` Python package can render.
   On Debian/Ubuntu: sudo apt install graphviz
3. Build or install tree-sitter grammars for C++ and Go:
   - Option A (recommended): pip install tree-sitter-languages or tree-sitter-languages (binary wheels)
   - Option B: clone grammars and build a shared library:
     python -c "from tree_sitter import Language; Language.build_library('build/my-languages.so', ['path/to/tree-sitter-go', 'path/to/tree-sitter-cpp'])"
4. Run server:
   python app.py
5. POST /generate with JSON {"lang":"go","code":"..."} -> returns SVG

See parser/ for language adapters. Add new language by creating a parser that implements ParserBase.parse(code)->(nodes,edges).
