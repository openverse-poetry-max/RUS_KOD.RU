#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Библиотека работы со строками для РусКод.
Содержит более 80 функций для манипуляции строками.
"""

import re
import hashlib
import base64
from datetime import datetime

функции = {}

# === Базовые операции ===
функции['длина'] = lambda x: len(str(x))
функции['верхний_регистр'] = lambda s: str(s).upper()
функции['нижний_регистр'] = lambda s: str(s).lower()
функции['заголовок'] = lambda s: str(s).title()
функции['капитализировать'] = lambda s: str(s).capitalize()
функции['поменять_регистр'] = lambda s: str(s).swapcase()

# === Поиск и замена ===
функции['заменить'] = lambda s, old, new: str(s).replace(str(old), str(new))
функции['заменить_все'] = lambda s, old, new: str(s).replace(str(old), str(new))
функции['заменить_n'] = lambda s, old, new, n: str(s).replace(str(old), str(new), int(n))
функции['найти'] = lambda s, sub: str(s).find(str(sub))
функции['найти_справа'] = lambda s, sub: str(s).rfind(str(sub))
функции['содержит'] = lambda s, sub: str(sub) in str(s)
функции['начинается_с'] = lambda s, prefix: str(s).startswith(str(prefix))
функции['заканчивается_на'] = lambda s, suffix: str(s).endswith(str(suffix))
функции['подсчитать'] = lambda s, sub: str(s).count(str(sub))

# === Разбиение и объединение ===
функции['разделить'] = lambda s, sep=' ': str(s).split(sep)
функции['разделить_строки'] = lambda s: str(s).splitlines()
функции['объединить'] = lambda lst, sep='': sep.join(map(str, lst))
функции['разделить_по_пробелам'] = lambda s: str(s).split()

# === Извлечение подстрок ===
функции['подстрока'] = lambda s, start, end=None: str(s)[int(start):int(end) if end else None]
функции['первые'] = lambda s, n: str(s)[:int(n)]
функции['последние'] = lambda s, n: str(s)[-int(n):]
функции['средние'] = lambda s, start, length: str(s)[int(start):int(start)+int(length)]

# === Обрезка и очистка ===
функции['обрезать'] = lambda s: str(s).strip()
функции['обрезать_слева'] = lambda s: str(s).lstrip()
функции['обрезать_справа'] = lambda s: str(s).rstrip()
функции['обрезать_символ'] = lambda s, c: str(s).strip(str(c))
функции['удалить_пробелы'] = lambda s: re.sub(r'\s+', '', str(s))
функции['удалить_лишние_пробелы'] = lambda s: re.sub(r'\s+', ' ', str(s)).strip()

# === Повторение и вставка ===
функции['повторить'] = lambda s, n: str(s) * int(n)
функции['вставить'] = lambda s, idx, sub: str(s)[:int(idx)] + str(sub) + str(s)[int(idx):]
функции['добавить_слева'] = lambda s, sub: str(sub) + str(s)
функции['добавить_справа'] = lambda s, sub: str(s) + str(sub)

# === Форматирование ===
функции['форматировать'] = lambda template, *args: str(template).format(*args)
функции['форматировать_именованно'] = lambda template, **kwargs: str(template).format(**kwargs)
функции['дополнить_слева'] = lambda s, width, fill=' ': str(s).rjust(int(width), str(fill))
функции['дополнить_справа'] = lambda s, width, fill=' ': str(s).ljust(int(width), str(fill))
функции['центрировать'] = lambda s, width, fill=' ': str(s).center(int(width), str(fill))
функции['заполнить_нулями'] = lambda s, width: str(s).zfill(int(width))

# === Числовое форматирование ===
def _формат_число(num, decimals=2, sep=' ', dec_sep='.'):
    num = float(num)
    целая = int(abs(num))
    дробная = abs(num) - целая
    знак = '-' if num < 0 else ''
    целая_стр = f"{целая:,}".replace(',', sep)
    if decimals > 0:
        дробная_стр = f"{дробная:.{decimals}f}"[2:]
        return f"{знак}{целая_стр}{dec_sep}{дробная_стр}"
    return f"{знак}{целая_стр}"

функции['формат_число'] = _формат_число
функции['формат_валюта'] = lambda num, currency='₽': f"{_формат_число(num)} {currency}"
функции['формат_проценты'] = lambda num, decimals=1: f"{float(num)*100:.{decimals}f}%"

# === Валидация ===
функции['это_цифра'] = lambda s: str(s).isdigit()
функции['это_буква'] = lambda s: str(s).isalpha()
функции['это_alnum'] = lambda s: str(s).isalnum()
функции['это_пробел'] = lambda s: str(s).isspace()
функции['это_число'] = lambda s: str(s).replace('.', '').replace('-', '').isdigit()

def _валидный_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, str(email)))

функции['валидный_email'] = _валидный_email

def _валидный_телефон(phone):
    pattern = r'^[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,4}[-\s\.]?[0-9]{1,9}$'
    return bool(re.match(pattern, re.sub(r'\s', '', str(phone))))

функции['валидный_телефон'] = _валидный_телефон

def _валидный_url(url):
    pattern = r'^https?://[^\s]+$'
    return bool(re.match(pattern, str(url)))

функции['валидный_url'] = _валидный_url

# === Хэширование ===
функции['хэш_md5'] = lambda s: hashlib.md5(str(s).encode()).hexdigest()
функции['хэш_sha1'] = lambda s: hashlib.sha1(str(s).encode()).hexdigest()
функции['хэш_sha256'] = lambda s: hashlib.sha256(str(s).encode()).hexdigest()
функции['хэш_sha512'] = lambda s: hashlib.sha512(str(s).encode()).hexdigest()

# === Кодирование ===
функции['кодировать_base64'] = lambda s: base64.b64encode(str(s).encode()).decode()
функции['декодировать_base64'] = lambda s: base64.b64decode(str(s).encode()).decode()
функции['кодировать_url'] = lambda s: __import__('urllib.parse').parse.quote(str(s))
функции['декодировать_url'] = lambda s: __import__('urllib.parse').parse.unquote(str(s))

# === Генерация ===
def _генератор_пароля(length=12, use_digits=True, use_special=False):
    import random
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if use_digits:
        chars += '0123456789'
    if use_special:
        chars += '!@#$%^&*()_+-=[]{}|;:,.<>?'
    return ''.join(random.choice(chars) for _ in range(int(length)))

функции['генератор_пароля'] = _генератор_пароля

def _случайная_строка(length=10):
    import random
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(chars) for _ in range(int(length)))

функции['случайная_строка'] = _случайная_строка

# === Расстояние Левенштейна ===
def _расстояние_левенштейна(s1, s2):
    if len(s1) < len(s2):
        return _расстояние_левенштейна(s2, s1)
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

функции['расстояние_левенштейна'] = _расстояние_левенштейна
функции['сходство_строк'] = lambda s1, s2: 1 - _расстояние_левенштейна(str(s1), str(s2)) / max(len(str(s1)), len(str(s2)), 1)

# === Шифрование Цезаря ===
def _шифр_цезаря(text, shift):
    result = ''
    for char in str(text):
        if char.isalpha():
            base = ord('А') if char.isupper() and ord('А') <= ord(char) <= ord('Я') else \
                   ord('а') if char.islower() and ord('а') <= ord(char) <= ord('я') else \
                   ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + int(shift)) % 32 + base)
        else:
            result += char
    return result

функции['шифр_цезаря'] = _шифр_цезаря
функции['дешифр_цезаря'] = lambda text, shift: _шифр_цезаря(text, -shift)

# === Палиндром ===
функции['палиндром_ли'] = lambda s: str(s).lower().replace(' ', '') == str(s).lower().replace(' ', '')[::-1]

# === Анаграммы ===
функции['анаграмма_ли'] = lambda s1, s2: sorted(str(s1).lower()) == sorted(str(s2).lower())

# === Извлечение данных ===
def _извлечь_числа(s):
    return [int(x) for x in re.findall(r'-?\d+', str(s))]

функции['извлечь_числа'] = _извлечь_числа

def _извлечь_emails(s):
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(pattern, str(s))

функции['извлечь_emails'] = _извлечь_emails

def _извлечь_телефоны(s):
    pattern = r'\+?[\d\s\-\(\)]{10,}'
    return re.findall(pattern, str(s))

функции['извлечь_телефоны'] = _извлечь_телефоны

def _извлечь_urls(s):
    pattern = r'https?://[^\s]+'
    return re.findall(pattern, str(s))

функции['извлечь_urls'] = _извлечь_urls

# === Многострочные операции ===
функции['число_строк'] = lambda s: len(str(s).splitlines())
функции['первая_строка'] = lambda s: str(s).splitlines()[0] if str(s).splitlines() else ''
функции['последняя_строка'] = lambda s: str(s).splitlines()[-1] if str(s).splitlines() else ''

# === Обратные операции ===
функции['обратить_строку'] = lambda s: str(s)[::-1]
функции['обратить_слова'] = lambda s: ' '.join(str(s).split()[::-1])

# === Сравнивание ===
функции['равны_игнорируя_регистр'] = lambda s1, s2: str(s1).lower() == str(s2).lower()
функции['сравнить'] = lambda s1, s2: (str(s1) > str(s2)) - (str(s1) < str(s2))
