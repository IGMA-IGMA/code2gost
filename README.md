# code2gost
Server: code -> block diagram (ГОСТ)


## Быстрый старт


1. Создать виртуальное окружение и установить зависимости:


```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
2.Установить tree-sitter Python биндинг и собрать или установить грамматики (см. документацию py-tree-sitter). Для Go используем tree-sitter-go.

3.Запустить сервер:
```py
python app.py
```
POST /generate с JSON { "lang": "go", "code": "package main ..." } вернёт SVG с диаграммой.
