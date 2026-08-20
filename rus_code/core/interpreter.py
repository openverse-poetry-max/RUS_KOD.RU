#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
РусКод - Универсальный язык программирования на русском языке
Ядро интерпретатора с поддержкой естественного языка
Версия 2.0 - Расширенная версия с множеством библиотек
"""

import re
import math
import random
import datetime
import json
import os
import sys
from typing import Any, Dict, List, Optional, Callable, Union

class РусКодЯдро:
    """Основное ядро языка РусКод"""
    
    def __init__(self):
        self.переменные: Dict[str, Any] = {}
        self.функции: Dict[str, Callable] = {}
        self.библиотеки: Dict[str, Any] = {}
        self.результат: Any = None
        self.история: List[str] = []
        
        # Регистрация встроенных функций
        self._зарегистрировать_встроенные_функции()
        
    def _зарегистрировать_встроенные_функции(self):
        """Регистрация всех встроенных функций"""
        
        # === МАТЕМАТИЧЕСКИЕ ФУНКЦИИ ===
        self.функции['плюс'] = lambda a, b: a + b
        self.функции['минус'] = lambda a, b: a - b
        self.функции['умножить'] = lambda a, b: a * b
        self.функции['разделить'] = lambda a, b: a / b if b != 0 else 0
        self.функции['целое_от_деления'] = lambda a, b: a // b
        self.функции['остаток_от_деления'] = lambda a, b: a % b
        self.функции['степень'] = lambda a, b: a ** b
        self.функции['корень'] = lambda a: math.sqrt(a)
        self.функции['квадратный_корень'] = lambda a: math.sqrt(a)
        self.функции['кубический_корень'] = lambda a: a ** (1/3)
        self.функции['абсолютное_значение'] = lambda a: abs(a)
        self.функции['модуль'] = lambda a: abs(a)
        self.функции['округлить'] = lambda a, n=0: round(a, int(n))
        self.функции['округлить_вверх'] = lambda a: math.ceil(a)
        self.функции['округлить_вниз'] = lambda a: math.floor(a)
        self.функции['максимум'] = lambda *args: max(args)
        self.функции['минимум'] = lambda *args: min(args)
        self.функции['сумма'] = lambda lst: sum(lst)
        self.функции['среднее'] = lambda lst: sum(lst) / len(lst) if lst else 0
        self.функции['произведение'] = lambda lst: eval('*'.join(map(str, lst))) if lst else 1
        
        # Тригонометрия
        self.функции['синус'] = lambda a: math.sin(a)
        self.функции['косинус'] = lambda a: math.cos(a)
        self.функции['тангенс'] = lambda a: math.tan(a)
        self.функции['арксинус'] = lambda a: math.asin(a)
        self.функции['арккосинус'] = lambda a: math.acos(a)
        self.функции['арктангенс'] = lambda a: math.atan(a)
        self.функции['гипотенуза'] = lambda a, b: math.hypot(a, b)
        self.функции['перевести_в_радианы'] = lambda a: math.radians(a)
        self.функции['перевести_в_градусы'] = lambda a: math.degrees(a)
        
        # Логарифмы
        self.функции['логарифм'] = lambda a, base=math.e: math.log(a, base)
        self.функции['натуральный_логарифм'] = lambda a: math.log(a)
        self.функции['десятичный_логарифм'] = lambda a: math.log10(a)
        self.функции['двоичный_логарифм'] = lambda a: math.log2(a)
        
        # Константы
        self.функции['пи'] = lambda: math.pi
        self.функции['е'] = lambda: math.e
        self.функции['тау'] = lambda: math.tau
        
        # Случайные числа
        self.функции['случайное_число'] = lambda: random.random()
        self.функции['случайное_целое'] = lambda a, b: random.randint(a, b)
        self.функции['случайное_вещественное'] = lambda a, b: random.uniform(a, b)
        self.функции['выбрать_случайно'] = lambda lst: random.choice(lst)
        self.функции['перемешать'] = lambda lst: random.shuffle(lst) or lst
        
        # === ФУНКЦИИ СО СТРОКАМИ ===
        self.функции['длина'] = lambda s: len(str(s))
        self.функции['верхний_регистр'] = lambda s: str(s).upper()
        self.функции['нижний_регистр'] = lambda s: str(s).lower()
        self.функции['заглавные_буквы'] = lambda s: str(s).title()
        self.функции['обрезать_пробелы'] = lambda s: str(s).strip()
        self.функции['обрезать_слева'] = lambda s: str(s).lstrip()
        self.функции['обрезать_справа'] = lambda s: str(s).rstrip()
        self.функции['заменить'] = lambda s, old, new: str(s).replace(old, new)
        self.функции['разделить_строку'] = lambda s, sep=' ': str(s).split(sep)
        self.функции['соединить_строки'] = lambda lst, sep='': sep.join(map(str, lst))
        self.функции['найти_подстроку'] = lambda s, sub: str(s).find(sub)
        self.функции['содержит'] = lambda s, sub: sub in str(s)
        self.функции['начинается_с'] = lambda s, prefix: str(s).startswith(prefix)
        self.функции['заканчивается_на'] = lambda s, suffix: str(s).endswith(suffix)
        self.функции['взять_символы'] = lambda s, start, end=None: str(s)[start:end]
        self.функции['первый_символ'] = lambda s: str(s)[0] if s else ''
        self.функции['последний_символ'] = lambda s: str(s)[-1] if s else ''
        self.функции['перевернуть_строку'] = lambda s: str(s)[::-1]
        self.функции['повторить_строку'] = lambda s, n: str(s) * int(n)
        self.функции['код_символа'] = lambda s: ord(str(s)[0]) if s else 0
        self.функции['символ_из_кода'] = lambda code: chr(int(code))
        self.функции['подсчитать_вхождения'] = lambda s, sub: str(s).count(sub)
        
        # Форматирование
        self.функции['в_строку'] = lambda x: str(x)
        self.функции['в_число'] = lambda s: float(str(s).replace(',', '.'))
        self.функции['в_целое_число'] = lambda s: int(float(str(s).replace(',', '.')))
        self.функции['форматировать_число'] = lambda num, digits=2: f"{float(num):.{int(digits)}f}"
        
        # === ЛОГИЧЕСКИЕ ФУНКЦИИ ===
        self.функции['истина'] = lambda: True
        self.функции['ложь'] = lambda: False
        self.функции['не'] = lambda x: not x
        self.функции['и'] = lambda *args: all(args)
        self.функции['или'] = lambda *args: any(args)
        self.функции['равно'] = lambda a, b: a == b
        self.функции['не_равно'] = lambda a, b: a != b
        self.функции['больше'] = lambda a, b: a > b
        self.функции['меньше'] = lambda a, b: a < b
        self.функции['больше_или_равно'] = lambda a, b: a >= b
        self.функции['меньше_или_равно'] = lambda a, b: a <= b
        self.функции['между'] = lambda val, low, high: low <= val <= high
        
        # === ФУНКЦИИ СПИСКОВ ===
        self.функции['создать_список'] = lambda *args: list(args)
        self.функции['добавить_в_список'] = lambda lst, item: lst.append(item) or lst
        self.функции['удалить_из_списка'] = lambda lst, item: lst.remove(item) if item in lst else lst
        self.функции['вставить_в_список'] = lambda lst, idx, item: lst.insert(idx, item) or lst
        self.функции['очистить_список'] = lambda lst: lst.clear() or lst
        self.функции['копия_списка'] = lambda lst: lst.copy()
        self.функции['длина_списка'] = lambda lst: len(lst)
        self.функции['элемент_по_индексу'] = lambda lst, idx: lst[idx] if 0 <= idx < len(lst) else None
        self.функции['индекс_элемента'] = lambda lst, item: lst.index(item) if item in lst else -1
        self.функции['сортировать_список'] = lambda lst: sorted(lst)
        self.функции['обратить_список'] = lambda lst: lst[::-1]
        self.функции['фильтровать_список'] = lambda lst, func: [x for x in lst if func(x)]
        self.функции['преобразовать_список'] = lambda lst, func: [func(x) for x in lst]
        self.функции['содержит_элемент'] = lambda lst, item: item in lst
        self.функции['последний_элемент'] = lambda lst: lst[-1] if lst else None
        self.функции['первый_элемент'] = lambda lst: lst[0] if lst else None
        self.функции['взять_первые'] = lambda lst, n: lst[:n]
        self.функции['взять_последние'] = lambda lst, n: lst[-n:] if n > 0 else []
        self.функции['удалить_повторы'] = lambda lst: list(dict.fromkeys(lst))
        
        # === ФУНКЦИИ СЛОВАРЕЙ ===
        self.функции['создать_словарь'] = lambda **kwargs: kwargs
        self.функции['получить_из_словаря'] = lambda d, key, default=None: d.get(key, default)
        self.функции['добавить_в_словарь'] = lambda d, key, value: d.__setitem__(key, value) or d
        self.функции['удалить_из_словаря'] = lambda d, key: d.pop(key, None) or d
        self.функции['ключи_словаря'] = lambda d: list(d.keys())
        self.функции['значения_словаря'] = lambda d: list(d.values())
        self.функции['пары_словаря'] = lambda d: list(d.items())
        self.функции['размер_словаря'] = lambda d: len(d)
        self.функции['содержит_ключ'] = lambda d, key: key in d
        self.функции['очистить_словарь'] = lambda d: d.clear() or d
        self.функции['объединить_словари'] = lambda d1, d2: {**d1, **d2}
        
        # === ФУНКЦИИ ВРЕМЕНИ И ДАТЫ ===
        self.функции['текущее_время'] = lambda: datetime.datetime.now().time()
        self.функции['текущая_дата'] = lambda: datetime.datetime.now().date()
        self.функции['текущая_дата_и_время'] = lambda: datetime.datetime.now()
        self.функции['год'] = lambda dt=None: (dt or datetime.datetime.now()).year
        self.функции['месяц'] = lambda dt=None: (dt or datetime.datetime.now()).month
        self.функции['день'] = lambda dt=None: (dt or datetime.datetime.now()).day
        self.функции['час'] = lambda dt=None: (dt or datetime.datetime.now()).hour
        self.функции['минута'] = lambda dt=None: (dt or datetime.datetime.now()).minute
        self.функции['секунда'] = lambda dt=None: (dt or datetime.datetime.now()).second
        self.функции['день_недели'] = lambda dt=None: (dt or datetime.datetime.now()).weekday()
        self.функции['название_дня_недели'] = lambda dt=None: ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье'][(dt or datetime.datetime.now()).weekday()]
        self.функции['название_месяца'] = lambda dt=None: ['', 'январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь'][(dt or datetime.datetime.now()).month]
        self.функции['форматировать_дату'] = lambda dt=None, fmt='%Y-%m-%d': (dt or datetime.datetime.now()).strftime(fmt)
        self.функции['разница_дат'] = lambda d1, d2: (d1 - d2).days
        
        # === ФУНКЦИИ ВВОДА-ВЫВОДА ===
        self.функции['написать_строку'] = lambda *args: print(' '.join(map(str, args))) or None
        self.функции['написать'] = lambda *args: print(' '.join(map(str, args)), end='') or None
        self.функции['напечатать'] = lambda *args: print(' '.join(map(str, args))) or None
        self.функции['спросить'] = lambda prompt='': input(prompt)
        self.функции['спросить_число'] = lambda prompt='': float(input(prompt).replace(',', '.'))
        self.функции['спросить_целое'] = lambda prompt='': int(float(input(prompt).replace(',', '.')))
        
        # === СИСТЕМНЫЕ ФУНКЦИИ ===
        self.функции['тип_данных'] = lambda x: type(x).__name__
        self.функции['проверить_тип'] = lambda x, t: type(x).__name__ == t
        self.функции['существует'] = lambda name: name in self.переменные
        self.функции['удалить_переменную'] = lambda name: self.переменные.pop(name, None) or True
        self.функции['список_переменных'] = lambda: list(self.переменные.keys())
        self.функции['очистить_все'] = lambda: self.переменные.clear() or True
        self.функции['помощь'] = lambda: self._показать_помощь()
        self.функции['версия'] = lambda: "РусКод 2.0"
        
        # === ФУНКЦИИ РАБОТЫ С ФАЙЛАМИ ===
        self.функции['прочитать_файл'] = lambda path: open(path, 'r', encoding='utf-8').read()
        self.функции['записать_файл'] = lambda path, content: open(path, 'w', encoding='utf-8').write(content) or True
        self.функции['добавить_в_файл'] = lambda path, content: open(path, 'a', encoding='utf-8').write(content) or True
        self.функции['существует_файл'] = lambda path: os.path.exists(path)
        self.функции['удалить_файл'] = lambda path: os.remove(path) if os.path.exists(path) else False
        self.функции['имя_файла'] = lambda path: os.path.basename(path)
        self.функции['путь_к_файлу'] = lambda path: os.path.dirname(path)
        self.функции['список_файлов'] = lambda path='.': os.listdir(path)
        self.функции['создать_папку'] = lambda path: os.makedirs(path, exist_ok=True) or True
        self.функции['удалить_папку'] = lambda path: os.rmdir(path) if os.path.exists(path) else False
        self.функции['текущая_папка'] = lambda: os.getcwd()
        self.функции['сменить_папку'] = lambda path: os.chdir(path) or True
        
        # === JSON ФУНКЦИИ ===
        self.функции['в_json'] = lambda obj: json.dumps(obj, ensure_ascii=False, indent=2)
        self.функции['из_json'] = lambda s: json.loads(s)
        self.функции['сохранить_json'] = lambda path, obj: json.dump(obj, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2) or True
        self.функции['загрузить_json'] = lambda path: json.load(open(path, 'r', encoding='utf-8'))
        
    def _показать_помощь(self):
        """Показать справку по доступным функциям"""
        print("\n=== РусКод - Доступные функции ===")
        categories = {
            'Математика': ['плюс', 'минус', 'умножить', 'разделить', 'степень', 'корень', 'синус', 'косинус', 'тангенс', 'логарифм', 'пи', 'е'],
            'Строки': ['длина', 'верхний_регистр', 'нижний_регистр', 'заменить', 'разделить_строку', 'соединить_строки', 'найти_подстроку'],
            'Списки': ['создать_список', 'добавить_в_список', 'сортировать_список', 'фильтровать_список', 'преобразовать_список'],
            'Словари': ['создать_словарь', 'получить_из_словаря', 'ключи_словаря', 'значения_словаря'],
            'Время': ['текущее_время', 'текущая_дата', 'год', 'месяц', 'день', 'час', 'минута'],
            'Ввод-Вывод': ['написать_строку', 'спросить', 'спросить_число'],
            'Файлы': ['прочитать_файл', 'записать_файл', 'существует_файл', 'список_файлов'],
            'JSON': ['в_json', 'из_json', 'сохранить_json', 'загрузить_json'],
            'Системные': ['тип_данных', 'помощь', 'версия', 'список_переменных']
        }
        for cat, funcs in categories.items():
            print(f"\n{cat}:")
            print(', '.join(funcs))
        return "Справка показана"
    
    def _разобрать_выражение(self, выражение: str) -> Any:
        """Разбор выражения с поддержкой естественного языка"""
        выражение = выражение.strip()
        
        # Пустое выражение
        if not выражение:
            return None
        
        # Числа (с поддержкой запятой для вещественных чисел)
        if re.match(r'^-?\d+\.?\d*$', выражение.replace(',', '.')):
            число = float(выражение.replace(',', '.'))
            return int(число) if число.is_integer() else число
        
        # Строковые литералы
        if (выражение.startswith('"') and выражение.endswith('"')) or \
           (выражение.startswith("'") and выражение.endswith("'")):
            return выражение[1:-1]
        
        # Булевы значения
        if выражение.lower() in ['истина', 'правда', 'да']:
            return True
        if выражение.lower() in ['ложь', 'неправда', 'нет']:
            return False
        
        # Вызов функции (проверяем до переменных)
        match = re.match(r'^([а-яА-ЯёЁ_]+)\((.*)\)$', выражение)
        if match:
            имя_функции = match.group(1)
            аргументы_str = match.group(2)
            
            if имя_функции in self.функции:
                аргументы = self._разобрать_аргументы(аргументы_str)
                try:
                    return self.функции[имя_функции](*аргументы)
                except Exception as e:
                    return f"Ошибка в функции {имя_функции}: {e}"
            else:
                return f"Неизвестная функция: {имя_функции}"
        
        # Переменные (проверяем после функций)
        if выражение in self.переменные:
            return self.переменные[выражение]
        
        # Массивы
        if выражение.startswith('[') and выражение.endswith(']'):
            содержимое = выражение[1:-1].strip()
            if not содержимое:
                return []
            элементы = self._разобрать_аргументы(содержимое)
            return элементы
        
        return выражение
    
    def _разобрать_аргументы(self, строка: str) -> List[Any]:
        """Разбор аргументов функции"""
        аргументы = []
        текущий = ""
        глубина = 0
        
        for символ in строка:
            if символ in '([{':
                глубина += 1
                текущий += символ
            elif символ in ')]}':
                глубина -= 1
                текущий += символ
            elif символ == ',' and глубина == 0:
                if текущий.strip():
                    аргументы.append(self._получить_значение(текущий.strip()))
                текущий = ""
            else:
                текущий += символ
        
        if текущий.strip():
            аргументы.append(self._получить_значение(текущий.strip()))
        
        return аргументы
    
    def _получить_значение(self, expr: str) -> Any:
        """Получить значение выражения (переменная, число, строка или функция)"""
        expr = expr.strip()
        
        # Число
        if re.match(r'^-?\d+\.?\d*$', expr.replace(',', '.')):
            число = float(expr.replace(',', '.'))
            return int(число) if число.is_integer() else число
        
        # Строка
        if (expr.startswith('"') and expr.endswith('"')) or \
           (expr.startswith("'") and expr.endswith("'")):
            return expr[1:-1]
        
        # Вызов функции
        match = re.match(r'^([а-яА-ЯёЁ_]+)\((.*)\)$', expr)
        if match:
            имя_функции = match.group(1)
            if имя_функции in self.функции:
                аргументы = self._разобрать_аргументы(match.group(2))
                try:
                    return self.функции[имя_функции](*аргументы)
                except Exception as e:
                    return f"Ошибка в функции {имя_функции}: {e}"
        
        # Переменная
        if expr in self.переменные:
            return self.переменные[expr]
        
        # Массив
        if expr.startswith('[') and expr.endswith(']'):
            содержимое = expr[1:-1].strip()
            if not содержимое:
                return []
            return self._разобрать_аргументы(содержимое)
        
        return expr
    
    def _выполнить_команду(self, команда: str) -> Any:
        """Выполнение одной команды"""
        команда = команда.strip()
        
        if not команда or команда.startswith('#'):
            return None
        
        # Присваивание: пусть x равна 5 / x = 5
        match = re.match(r'^(?:пусть\s+)?([а-яА-ЯёЁa-zA-Z_\d]+)\s+(?:равна|равно|=)\s+(.+)$', команда)
        if match:
            имя = match.group(1)
            значение = self._разобрать_выражение(match.group(2))
            self.переменные[имя] = значение
            return значение
        
        # Условие: если условие то команда
        match = re.match(r'^если\s+(.+?)\s+то\s+(.+)$', команда, re.IGNORECASE)
        if match:
            условие = self._разобрать_выражение(match.group(1))
            если_истина = match.group(2)
            if условие:
                return self._выполнить_команду(если_истина)
            return None
        
        # Условие с иначе
        match = re.match(r'^если\s+(.+?)\s+то\s+(.+?)\s+иначе\s+(.+)$', команда, re.IGNORECASE)
        if match:
            условие = self._разобрать_выражение(match.group(1))
            если_истина = match.group(2)
            если_ложь = match.group(3)
            if условие:
                return self._выполнить_команду(если_истина)
            else:
                return self._выполнить_команду(если_ложь)
        
        # Цикл: повторить N раз команду
        match = re.match(r'^повторить\s+(\d+)\s+раз\s+(.+)$', команда, re.IGNORECASE)
        if match:
            количество = int(match.group(1))
            тело = match.group(2)
            результат = None
            for i in range(количество):
                self.переменные['_i'] = i
                результат = self._выполнить_команду(тело)
            if '_i' in self.переменные:
                del self.переменные['_i']
            return результат
        
        # Цикл пока
        match = re.match(r'^пока\s+(.+?)\s+делать\s+(.+)$', команда, re.IGNORECASE)
        if match:
            условие_str = match.group(1)
            тело = match.group(2)
            результат = None
            while self._разобрать_выражение(условие_str):
                результат = self._выполнить_команду(тело)
            return результат
        
        # Для каждого в списке
        match = re.match(r'^для\s+каждого\s+([а-яА-ЯёЁ_\d]+)\s+в\s+(.+?)\s+делать\s+(.+)$', команда, re.IGNORECASE)
        if match:
            переменная = match.group(1)
            список = self._разобрать_выражение(match.group(2))
            тело = match.group(3)
            результат = None
            for элемент in список:
                self.переменные[переменная] = элемент
                результат = self._выполнить_команду(тело)
            return результат
        
        # Просто выражение
        return self._разобрать_выражение(команда)
    
    def выполнить(self, код: str) -> Any:
        """Выполнение программы"""
        строки = код.split('\n')
        результат = None
        
        for строка in строки:
            if строка.strip():
                результат = self._выполнить_команду(строка)
                self.история.append(строка)
        
        self.результат = результат
        return результат


def запустить_интерпретатор():
    """Запуск интерактивного интерпретатора"""
    ядро = РусКодЯдро()
    print("=" * 60)
    print("   РусКод v2.0 - Универсальный язык программирования")
    print("   Полностью на русском языке!")
    print("=" * 60)
    print("\nПримеры команд:")
    print("  пусть x равна 10")
    print("  написать_строку(плюс(x, 5))")
    print("  если больше(x, 5) то написать_строку('x больше 5')")
    print("  повторить 5 раз написать_строку('Привет!')")
    print("  помощь() - показать все доступные функции")
    print("\nВведите 'выход' для завершения\n")
    
    while True:
        try:
            ввод = input("РусКод >>> ").strip()
            if ввод.lower() in ['выход', 'exit', 'quit']:
                print("До свидания!")
                break
            if ввод:
                результат = ядро.выполнить(ввод)
                if результат is not None:
                    print(f"-> {результат}")
        except KeyboardInterrupt:
            print("\nДо свидания!")
            break
        except Exception as e:
            print(f"Ошибка: {e}")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Выполнение из файла
        файл = sys.argv[1]
        if os.path.exists(файл):
            with open(файл, 'r', encoding='utf-8') as f:
                код = f.read()
            ядро = РусКодЯдро()
            ядро.выполнить(код)
        else:
            print(f"Файл не найден: {файл}")
    else:
        # Интерактивный режим
        запустить_интерпретатор()

# Алиас для совместимости
Interpreter = РусКодЯдро
