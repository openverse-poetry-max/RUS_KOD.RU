#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Веб-IDE для языка программирования РусКод
Позволяет вставлять весь код сразу и запускать его одной кнопкой
"""

import sys
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import unquote
import json
import tempfile
import subprocess

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.interpreter import Interpreter

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>РусКод IDE - Программирование на русском</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        
        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .ide-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            height: calc(100vh - 200px);
        }
        
        .panel {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }
        
        .panel-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 20px;
            font-weight: bold;
            font-size: 1.1em;
        }
        
        .editor-container {
            flex: 1;
            position: relative;
        }
        
        #code-editor {
            width: 100%;
            height: 100%;
            border: none;
            padding: 20px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 14px;
            line-height: 1.5;
            resize: none;
            outline: none;
            background: #f8f9fa;
        }
        
        .output-container {
            flex: 1;
            padding: 20px;
            background: #1e1e1e;
            color: #00ff00;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 14px;
            overflow-y: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        
        .controls {
            display: flex;
            gap: 15px;
            margin-top: 20px;
            justify-content: center;
        }
        
        button {
            padding: 15px 40px;
            font-size: 1.1em;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .btn-run {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
        }
        
        .btn-run:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(56, 239, 125, 0.4);
        }
        
        .btn-clear {
            background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
            color: white;
        }
        
        .btn-clear:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(244, 92, 67, 0.4);
        }
        
        .btn-example {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }
        
        .btn-example:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(245, 87, 108, 0.4);
        }
        
        .status-bar {
            background: #f8f9fa;
            padding: 10px 20px;
            border-top: 1px solid #e9ecef;
            color: #6c757d;
            font-size: 0.9em;
        }
        
        .error {
            color: #ff6b6b;
        }
        
        .success {
            color: #51cf66;
        }
        
        .info {
            color: #339af0;
        }
        
        @media (max-width: 768px) {
            .ide-container {
                grid-template-columns: 1fr;
                height: auto;
            }
            
            .panel {
                height: 400px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🇷🇺 РусКод IDE</h1>
            <p>Универсальный язык программирования полностью на русском языке</p>
        </header>
        
        <div class="ide-container">
            <div class="panel">
                <div class="panel-header">📝 Редактор кода</div>
                <div class="editor-container">
                    <textarea id="code-editor" placeholder="Введите ваш код на русском языке здесь...

Пример:
пусть x равна 10
пусть y равна 20
пусть сумма равна плюс(x, y)
написать_строку(&quot;Сумма:&quot;, сумма)

повторить 5 раз
    написать_строку(&quot;Привет, мир!&quot;)
"></textarea>
                </div>
                <div class="status-bar">
                    Строк: <span id="line-count">0</span> | Позиция: <span id="cursor-pos">0</span>
                </div>
            </div>
            
            <div class="panel">
                <div class="panel-header">💻 Результат выполнения</div>
                <div class="output-container" id="output"></div>
                <div class="status-bar">
                    Статус: <span id="status">Готов к работе</span>
                </div>
            </div>
        </div>
        
        <div class="controls">
            <button class="btn-run" onclick="runCode()">▶ Запустить код</button>
            <button class="btn-example" onclick="loadExample()">📚 Загрузить пример</button>
            <button class="btn-clear" onclick="clearOutput()">🗑 Очистить вывод</button>
        </div>
    </div>
    
    <script>
        const editor = document.getElementById('code-editor');
        const output = document.getElementById('output');
        const status = document.getElementById('status');
        const lineCount = document.getElementById('line-count');
        const cursorPos = document.getElementById('cursor-pos');
        
        // Обновление счетчиков
        editor.addEventListener('input', () => {
            const lines = editor.value.split('\\n').length;
            lineCount.textContent = lines;
        });
        
        editor.addEventListener('click', () => {
            cursorPos.textContent = editor.selectionStart;
        });
        
        editor.addEventListener('keyup', () => {
            cursorPos.textContent = editor.selectionStart;
        });
        
        // Загрузка примера
        function loadExample() {
            const example = `// Пример программы на РусКод
// Эта программа демонстрирует основные возможности языка

// Объявление переменных
пусть имя равна "Александр"
пусть возраст равна 25
пусть рост равна 175.5

// Вывод информации
написать_строку("Привет, меня зовут", имя)
написать_строку("Мне", возраст, "лет")
написать_строку("Мой рост:", рост, "см")

// Математические операции
пусть год_рождения равна вычесть(2024, возраст)
написать_строку("Я родился в", год_рождения, "году")

// Условия
если больше(возраст, 18) то
    написать_строку("Я совершеннолетний")
иначе
    написать_строку("Я еще несовершеннолетний")

// Циклы
написать_строку("\\nТаблица умножения на 5:")
пусть i равна 1
пока меньше_или_равно(i, 10)
    пусть результат равна умножить(i, 5)
    написать_строку(i, "× 5 =", результат)
    пусть i равна плюс(i, 1)

// Работа со строками
пусть текст равна "Программирование на русском языке"
написать_строку("\\nОригинальный текст:", текст)
написать_строку("Длина текста:", длина(текст))
написать_строку("В верхнем регистре:", верхний_регистр(текст))

// Списки
пусть числа равна [1, 2, 3, 4, 5]
написать_строку("\\nСписок чисел:", числа)
написать_строку("Сумма элементов:", сумма_списка(числа))
написать_строку("Максимум:", максимум_списка(числа))

// Факториал
написать_строку("\\nФакториалы от 1 до 10:")
пусть n равна 1
повторить 10 раз
    написать_строку(n, "! =", факториал(n))
    пусть n равна плюс(n, 1)

написать_строку("\\n✅ Программа завершена успешно!")
`;
            editor.value = example;
            editor.dispatchEvent(new Event('input'));
            status.textContent = "Пример загружен";
            status.className = "info";
        }
        
        // Запуск кода
        async function runCode() {
            const code = editor.value;
            
            if (!code.trim()) {
                output.textContent = "❌ Ошибка: Введите код для выполнения";
                status.textContent = "Ошибка";
                status.className = "error";
                return;
            }
            
            status.textContent = "Выполнение...";
            status.className = "info";
            output.textContent = "Запуск программы...\\n" + "=".repeat(50) + "\\n\\n";
            
            try {
                const response = await fetch('/execute', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ code: code }),
                });
                
                const result = await response.json();
                
                if (result.success) {
                    output.textContent += result.output;
                    status.textContent = "✅ Выполнено успешно";
                    status.className = "success";
                } else {
                    output.textContent += "❌ Ошибка:\\n" + result.error;
                    status.textContent = "Ошибка выполнения";
                    status.className = "error";
                }
            } catch (error) {
                output.textContent += "❌ Ошибка соединения: " + error.message;
                status.textContent = "Ошибка соединения";
                status.className = "error";
            }
        }
        
        // Очистка вывода
        function clearOutput() {
            output.textContent = "";
            status.textContent = "Вывод очищен";
            status.className = "";
        }
        
        // Инициализация
        lineCount.textContent = editor.value.split('\\n').length;
    </script>
</body>
</html>
"""

class RusCodeHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode('utf-8'))
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/execute':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                code = data.get('code', '')
                
                # Создаем интерпретатор
                interpreter = Interpreter()
                
                # Перехватываем вывод
                import io
                from contextlib import redirect_stdout
                
                f = io.StringIO()
                with redirect_stdout(f):
                    try:
                        interpreter.выполнить(code)
                        success = True
                        error = None
                    except Exception as e:
                        success = False
                        error = str(e)
                
                output = f.getvalue()
                
                response = {
                    'success': success,
                    'output': output,
                    'error': error
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                
            except Exception as e:
                response = {
                    'success': False,
                    'output': '',
                    'error': f'Ошибка обработки запроса: {str(e)}'
                }
                
                self.send_response(500)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {format % args}")

def start_server(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, RusCodeHandler)
    print(f"🚀 Веб-IDE РусКод запущена!")
    print(f"📍 Откройте в браузере: http://localhost:{port}")
    print(f"📝 Вставляйте весь код сразу и нажимайте 'Запустить код'")
    print(f"⏹  Для остановки нажмите Ctrl+C")
    print("=" * 60)
    httpd.serve_forever()

if __name__ == '__main__':
    port = 8080
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Неверный номер порта: {sys.argv[1]}")
            sys.exit(1)
    
    start_server(port)
