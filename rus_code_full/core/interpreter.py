#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
РусКод - Универсальный язык программирования на русском языке.
Ядро интерпретатора с поддержкой библиотек, функций и естественного языка.
"""

import sys
import os
import re
import math
import json
import random
import datetime
import time
from pathlib import Path

# Добавляем пути для поиска модулей
SCRIPT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCRIPT_DIR / 'libs'))
sys.path.insert(0, str(SCRIPT_DIR / 'modules'))

class РусКодИнтерпретатор:
    def __init__(self):
        self.переменные = {}
        self.функции = {}
        self.библиотеки = {}
        self.загруженные_модули = set()
        self.результат = None
        
        # Регистрация встроенных функций
        self._зарегистрировать_встроенные_функции()
    
    def _зарегистрировать_встроенные_функции(self):
        """Регистрация всех встроенных функций языка"""
        
        # Математические функции с авто-конвертацией
        def _конвертировать_число(x):
            try:
                return float(x)
            except (ValueError, TypeError):
                # Если это имя переменной, пытаемся найти её в функциях
                if str(x) in self.функции:
                    результат = self.функции[str(x)]()
                    return float(результат) if isinstance(результат, (int, float)) else 0
                return 0
        
        self.функции['плюс'] = lambda *args: sum(_конвертировать_число(x) for x in args) if args else 0
        self.функции['минус'] = lambda a, b=0: _конвертировать_число(a) - _конвертировать_число(b)
        self.функции['умножить'] = lambda *args: eval('*'.join(str(_конвертировать_число(x)) for x in args)) if args else 1
        self.функции['разделить'] = lambda a, b: _конвертировать_число(a) / _конвертировать_число(b) if _конвертировать_число(b) != 0 else 0
        self.функции['степень'] = lambda a, b: _конвертировать_число(a) ** _конвертировать_число(b)
        self.функции['корень'] = lambda x, n=2: _конвертировать_число(x) ** (1/_конвертировать_число(n))
        self.функции['модуль'] = lambda x: abs(_конвертировать_число(x))
        self.функции['округлить'] = lambda x, n=0: round(_конвертировать_число(x), int(_конвертировать_число(n)))
        self.функции['целое'] = lambda x: int(_конвертировать_число(x))
        self.функции['дробное'] = lambda x: float(_конвертировать_число(x))
        self.функции['случайное'] = lambda a=0, b=1: random.uniform(_конвертировать_число(a), _конвертировать_число(b))
        self.функции['случайное_целое'] = lambda a, b: random.randint(int(_конвертировать_число(a)), int(_конвертировать_число(b)))
        self.функции['максимум'] = lambda *args: max(_конвертировать_число(x) for x in args) if args else 0
        self.функции['минимум'] = lambda *args: min(_конвертировать_число(x) for x in args) if args else 0
        self.функции['сумма'] = lambda lst: sum(_конвертировать_число(x) for x in lst)
        self.функции['среднее'] = lambda lst: sum(_конвертировать_число(x) for x in lst) / len(lst) if lst else 0
        
        # Функции работы со строками
        self.функции['длина'] = lambda x: len(str(x))
        self.функции['верхний_регистр'] = lambda s: str(s).upper()
        self.функции['нижний_регистр'] = lambda s: str(s).lower()
        self.функции['заменить'] = lambda s, old, new: str(s).replace(str(old), str(new))
        self.функции['разделить'] = lambda s, sep=' ': str(s).split(sep)
        self.функции['объединить'] = lambda lst, sep='': sep.join(map(str, lst))
        self.функции['подстрока'] = lambda s, start, end=None: str(s)[int(start):int(end) if end else None]
        self.функции['найти'] = lambda s, sub: str(s).find(str(sub))
        self.функции['начинается_с'] = lambda s, prefix: str(s).startswith(str(prefix))
        self.функции['заканчивается_на'] = lambda s, suffix: str(s).endswith(str(suffix))
        self.функции['обрезать'] = lambda s: str(s).strip()
        self.функции['повторить'] = lambda s, n: str(s) * int(n)
        
        # Функции ввода-вывода
        self.функции['написать_строку'] = lambda *args: print(' '.join(map(str, args)))
        self.функции['написать'] = lambda *args: print(' '.join(map(str, args)), end='')
        self.функции['спросить'] = lambda prompt="": input(str(prompt) + " ")
        self.функции['спросить_число'] = lambda prompt="": float(input(str(prompt) + " "))
        self.функции['спросить_целое'] = lambda prompt="": int(input(str(prompt) + " "))
        
        # Функции работы со списками
        self.функции['создать_список'] = lambda *args: list(args)
        self.функции['добавить'] = lambda lst, item: lst.append(item) or lst
        self.функции['удалить'] = lambda lst, item: (lst.remove(item) if item in lst else lst) or lst
        self.функции['вставить'] = lambda lst, idx, item: lst.insert(int(idx), item) or lst
        self.функции['получить'] = lambda lst, idx: lst[int(idx)] if 0 <= int(idx) < len(lst) else None
        self.функции['длина_списка'] = lambda lst: len(lst)
        self.функции['сортировать'] = lambda lst: sorted(lst)
        self.функции['обратить'] = lambda lst: lst[::-1]
        self.функции['срез'] = lambda lst, start, end=None: lst[int(start):int(end) if end else None]
        
        # Логические функции
        self.функции['больше'] = lambda a, b: a > b
        self.функции['меньше'] = lambda a, b: a < b
        self.функции['равно'] = lambda a, b: a == b
        self.функции['не_равно'] = lambda a, b: a != b
        self.функции['больше_или_равно'] = lambda a, b: a >= b
        self.функции['меньше_или_равно'] = lambda a, b: a <= b
        self.функции['и'] = lambda a, b: a and b
        self.функции['или'] = lambda a, b: a or b
        self.функции['не'] = lambda a: not a
        self.функции['истина'] = lambda: True
        self.функции['ложь'] = lambda: False
        
        # Функции работы с датой и временем
        self.функции['текущая_дата'] = lambda: datetime.date.today().isoformat()
        self.функции['текущее_время'] = lambda: datetime.datetime.now().strftime("%H:%M:%S")
        self.функции['текущая_дата_время'] = lambda: datetime.datetime.now().isoformat()
        self.функции['форматировать_дату'] = lambda d, fmt="%Y-%m-%d": datetime.datetime.fromisoformat(d).strftime(fmt) if isinstance(d, str) else d.strftime(fmt)
        self.функции['секунды'] = lambda: time.time()
        self.функции['пауза'] = lambda sec: time.sleep(float(sec))
        
        # Функции работы с файлами
        self.функции['прочитать_файл'] = lambda path: open(path, 'r', encoding='utf-8').read()
        self.функции['записать_файл'] = lambda path, content: open(path, 'w', encoding='utf-8').write(str(content))
        self.функции['добавить_в_файл'] = lambda path, content: open(path, 'a', encoding='utf-8').write(str(content))
        self.функции['существует_файл'] = lambda path: os.path.exists(path)
        self.функции['удалить_файл'] = lambda path: os.remove(path) if os.path.exists(path) else False
        self.функции['имя_файла'] = lambda path: os.path.basename(path)
        self.функции['путь_к_файлу'] = lambda path: os.path.abspath(path)
        
        # Функции работы с JSON
        self.функции['в_json'] = lambda obj: json.dumps(obj, ensure_ascii=False)
        self.функции['из_json'] = lambda s: json.loads(s)
        self.функции['сохранить_json'] = lambda path, obj: json.dump(obj, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        self.функции['загрузить_json'] = lambda path: json.load(open(path, 'r', encoding='utf-8'))
        
        # Системные функции
        self.функции['тип'] = lambda x: type(x).__name__
        self.функции['диапазон'] = lambda start, end=None, step=1: list(range(int(start), int(end) if end else int(start), int(step))) if end else list(range(int(start)))
        self.функции['перечислить'] = lambda lst: list(enumerate(lst))
        self.функции['ключи'] = lambda d: list(d.keys()) if isinstance(d, dict) else []
        self.функции['значения'] = lambda d: list(d.values()) if isinstance(d, dict) else []
        self.функции['пары'] = lambda d: list(d.items()) if isinstance(d, dict) else []
        self.функции['пусто'] = lambda x: len(x) == 0 if hasattr(x, '__len__') else not x
    
    def загрузить_библиотеку(self, имя):
        """Загрузка внешней библиотеки"""
        возможные_имена = [
            f"{имя}",
            f"{имя}_lib",
            f"libs.{имя}",
            f"modules.{имя}"
        ]
        
        for имя_модуля in возможные_имена:
            try:
                модуль = __import__(имя_модуля.replace('/', '.'))
                if hasattr(модуль, 'функции'):
                    self.функции.update(модуль.функции)
                    self.загруженные_модули.add(имя)
                    return True
                elif hasattr(модуль, '__dict__'):
                    # Ищем функции в модуле
                    for имя_функ, функ in модуль.__dict__.items():
                        if callable(функ) and not имя_функ.startswith('_'):
                            self.функции[имя_функ] = функ
                    self.загруженные_модули.add(имя)
                    return True
            except ImportError:
                continue
            except Exception as e:
                print(f"Ошибка загрузки библиотеки {имя}: {e}")
                continue
        
        # Пробуем загрузить как файл
        путь_к_файлу = SCRIPT_DIR / f"{имя}.py"
        if not путь_к_файлу.exists():
            путь_к_файлу = SCRIPT_DIR / 'libs' / f"{имя}.py"
        if not путь_к_файлу.exists():
            путь_к_файлу = SCRIPT_DIR / 'modules' / f"{имя}.py"
        
        if путь_к_файлу.exists():
            import importlib.util
            spec = importlib.util.spec_from_file_location(имя, путь_к_файлу)
            модуль = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(модуль)
            
            if hasattr(модуль, 'функции'):
                self.функции.update(модуль.функции)
            else:
                for имя_функ, функ in модуль.__dict__.items():
                    if callable(функ) and not имя_функ.startswith('_'):
                        self.функции[имя_функ] = функ
            
            self.загруженные_модули.add(имя)
            return True
        
        raise ImportError(f"Библиотека '{имя}' не найдена")
    
    def _выполнить_выражение(self, выражение):
        """Выполнение одного выражения"""
        выражение = выражение.strip()
        
        if not выражение or выражение.startswith('#'):
            return None
        
        # Обработка импорта библиотек (с поддержкой латиницы для имён библиотек)
        импорт_паттерн = r'^использовать\s+([а-яА-ЯёЁa-zA-Z0-9_\s,]+)$'
        совпадение = re.match(импорт_паттерн, выражение)
        if совпадение:
            библиотеки = [б.strip() for б in совпадение.group(1).split(',')]
            for биб in библиотеки:
                self.загрузить_библиотеку(биб)
            return None
        
        # Обработка присваивания переменных
        присваивание_паттерн = r'^пусть\s+([а-яА-ЯёЁ0-9_]+)\s+(равна|равно|это)\s+(.+)$'
        совпадение = re.match(присваивание_паттерн, выражение, re.IGNORECASE)
        if совпадение:
            имя = совпадение.group(1)
            значение = self._вычислить(совпадение.group(3))
            self.переменные[имя] = значение
            return значение
        
        # Прямое присваивание (x = значение)
        прямое_присваивание = r'^([а-яА-ЯёЁ0-9_]+)\s*=\s*(.+)$'
        совпадение = re.match(прямое_присваивание, выражение)
        if совпадение:
            имя = совпадение.group(1)
            значение = self._вычислить(совпадение.group(2))
            self.переменные[имя] = значение
            return значение
        
        # Обработка условий
        если_паттерн = r'^если\s+(.+?)\s+то\s+(.+?)(?:\s+иначе\s+(.+))?$'
        совпадение = re.match(если_паттерн, выражение, re.IGNORECASE | re.DOTALL)
        if совпадение:
            условие = self._вычислить(совпадение.group(1))
            if условие:
                return self._выполнить_блок(совпадение.group(2))
            elif совпадение.group(3):
                return self._выполнить_блок(совпадение.group(3))
            return None
        
        # Обработка циклов
        цикл_паттерн = r'^повторить\s+(\d+)\s+раз\s+(.+)$'
        совпадение = re.match(цикл_паттерн, выражение, re.IGNORECASE | re.DOTALL)
        if совпадение:
            количество = int(совпадение.group(1))
            тело = совпадение.group(2)
            результат = None
            for _ in range(количество):
                результат = self._выполнить_блок(тело)
            return результат
        
        цикл_пока_паттерн = r'^пока\s+(.+?)\s+делать\s+(.+)$'
        совпадение = re.match(цикл_пока_паттерн, выражение, re.IGNORECASE | re.DOTALL)
        if совпадение:
            условие = совпадение.group(1)
            тело = совпадение.group(2)
            результат = None
            while self._вычислить(условие):
                результат = self._выполнить_блок(тело)
            return результат
        
        цикл_для_паттерн = r'^для\s+([а-яА-ЯёЁ0-9_]+)\s+из\s+(.+?)\s+делать\s+(.+)$'
        совпадение = re.match(цикл_для_паттерн, выражение, re.IGNORECASE | re.DOTALL)
        if совпадение:
            переменная = совпадение.group(1)
            коллекция = self._вычислить(совпадение.group(2))
            тело = совпадение.group(3)
            результат = None
            for элемент in коллекция:
                self.переменные[переменная] = элемент
                результат = self._выполнить_блок(тело)
            return результат
        
        # Вызов функции
        вызов_функ = r'^([а-яА-ЯёЁ0-9_]+)\s*\(([^)]*)\)$'
        совпадение = re.match(вызов_функ, выражение)
        if совпадение:
            имя_функ = совпадение.group(1)
            аргументы = [self._вычислить(арг.strip()) for арг in совпадение.group(2).split(',') if арг.strip()]
            
            if имя_функ in self.функции:
                return self.функции[имя_функ](*аргументы)
            else:
                raise NameError(f"Функция '{имя_функ}' не найдена")
        
        # Просто вычисление выражения
        return self._вычислить(выражение)
    
    def _вычислить(self, выражение):
        """Вычисление значения выражения"""
        выражение = str(выражение).strip()
        
        # Сначала пытаемся вычислить как вызов функции
        вызов_функ = r'^([а-яА-ЯёЁ0-9_]+)\s*\(([^)]*)\)$'
        совпадение = re.match(вызов_функ, выражение)
        if совпадение:
            имя_функ = совпадение.group(1)
            аргументы = [self._вычислить(арг.strip()) for арг in совпадение.group(2).split(',') if арг.strip()]
            
            if имя_функ in self.функции:
                return self.функции[имя_функ](*аргументы)
            else:
                raise NameError(f"Функция '{имя_функ}' не найдена")
        
        # Замена переменных - сначала длинные имена, потом короткие
        отсортированные_имена = sorted(self.переменные.keys(), key=len, reverse=True)
        for имя in отсортированные_имена:
            значение = self.переменные[имя]
            паттерн = r'\b' + имя + r'\b'
            if isinstance(значение, str):
                выражение = re.sub(паттерн, f"'{значение}'", выражение)
            else:
                выражение = re.sub(паттерн, str(значение), выражение)
        
        # Повторно пытаемся вычислить вызовы функций после подстановки переменных
        вызов_функ2 = r'^([а-яА-ЯёЁ0-9_]+)\s*\(([^)]*)\)$'
        совпадение2 = re.match(вызов_функ2, выражение)
        if совпадение2:
            имя_функ = совпадение2.group(1)
            аргументы = [self._вычислить(арг.strip()) for арг in совпадение2.group(2).split(',') if арг.strip()]
            
            if имя_функ in self.функции:
                return self.функции[имя_функ](*аргументы)
        
        # Замена логических операторов
        выражение = выражение.replace(' и ', ' and ')
        выражение = выражение.replace(' или ', ' or ')
        выражение = выражение.replace(' не ', ' not ')
        выражение = выражение.replace('истина', 'True')
        выражение = выражение.replace('ложь', 'False')
        
        try:
            # Безопасное вычисление
            результат = eval(выражение, {"__builtins__": {}}, self.функции)
            return результат
        except:
            # Если не удалось вычислить, возвращаем как строку
            if выражение.startswith("'") and выражение.endswith("'"):
                return выражение[1:-1]
            if выражение.startswith('"') and выражение.endswith('"'):
                return выражение[1:-1]
            return выражение
    
    def _выполнить_блок(self, блок):
        """Выполнение блока кода (может содержать несколько выражений)"""
        блок = блок.strip()
        результат = None
        
        # Разделяем на строки
        строки = блок.split('\n')
        
        for строка in строки:
            строка = строка.strip()
            if строка:
                результат = self._выполнить_выражение(строка)
        
        return результат
    
    def выполнить(self, код):
        """Выполнение всего кода программы"""
        строки = код.split('\n')
        текущий_блок = []
        результат = None
        
        i = 0
        while i < len(строки):
            строка = строки[i].strip()
            
            # Пропускаем пустые строки и комментарии
            if not строка or строка.startswith('#'):
                i += 1
                continue
            
            # Проверяем многострочные конструкции
            if строка.startswith('если') and 'то' in строка:
                # Собираем весь блок если-иначе
                блок = [строка]
                уровень = 1
                i += 1
                while i < len(строки) and уровень > 0:
                    текущая = строки[i]
                    блок.append(текущая)
                    if текущая.strip().startswith('если'):
                        уровень += 1
                    elif текущая.strip().startswith('конец_если'):
                        уровень -= 1
                    i += 1
                
                полный_блок = '\n'.join(блок)
                # Убираем маркеры начала и конца
                import re as ре
                полный_блок = ре.sub(r'^если\s+', 'если ', полный_блок, flags=re.MULTILINE)
                полный_блок = ре.sub(r'\s+конец_если$', '', полный_блок, flags=re.MULTILINE)
                
                результат = self._выполнить_выражение(полный_блок)
                continue
            
            elif строка.startswith('повторить') and 'раз' in строка:
                блок = [строка]
                i += 1
                while i < len(строки):
                    текущая = строки[i].strip()
                    if not текущая or текущая.startswith('#'):
                        блок.append(строки[i])
                        i += 1
                        continue
                    # Проверяем, не началась ли новая конструкция
                    if any(текущая.startswith(к) for к in ['если', 'повторить', 'пока', 'для', 'функция']):
                        break
                    блок.append(строки[i])
                    i += 1
                
                результат = self._выполнить_выражение('\n'.join(блок))
                continue
            
            elif строка.startswith('пока') and 'делать' in строка:
                блок = [строка]
                i += 1
                while i < len(строки):
                    текущая = строки[i].strip()
                    if not текущая or текущая.startswith('#'):
                        блок.append(строки[i])
                        i += 1
                        continue
                    if any(текущая.startswith(к) for к in ['если', 'повторить', 'пока', 'для', 'функция']):
                        break
                    блок.append(строки[i])
                    i += 1
                
                результат = self._выполнить_выражение('\n'.join(блок))
                continue
            
            elif строка.startswith('для') and 'делать' in строка:
                блок = [строка]
                i += 1
                while i < len(строки):
                    текущая = строки[i].strip()
                    if not текущая or текущая.startswith('#'):
                        блок.append(строки[i])
                        i += 1
                        continue
                    if any(текущая.startswith(к) for к in ['если', 'повторить', 'пока', 'для', 'функция']):
                        break
                    блок.append(строки[i])
                    i += 1
                
                результат = self._выполнить_выражение('\n'.join(блок))
                continue
            
            # Обычная строка
            результат = self._выполнить_выражение(строка)
            i += 1
        
        return результат


def главный():
    """Точка входа для запуска из терминала"""
    if len(sys.argv) < 2:
        print("РусКод - Универсальный язык программирования на русском языке")
        print("Использование: рускод <имя_файла> [аргументы]")
        print("   или: python -m core.interpreter <имя_файла>")
        print("\nПримеры:")
        print("  рускод программа.рк")
        print("  рускод примеры/калькулятор.рк")
        sys.exit(1)
    
    имя_файла = sys.argv[1]
    
    # Проверяем существование файла
    путь = Path(имя_файла)
    if not путь.exists():
        # Пробуем найти в директории examples
        путь = SCRIPT_DIR / 'examples' / имя_файла
        if not путь.exists():
            print(f"Ошибка: Файл '{имя_файла}' не найден")
            sys.exit(1)
    
    # Читаем файл
    try:
        with open(путь, 'r', encoding='utf-8') as f:
            код = f.read()
    except Exception as e:
        print(f"Ошибка чтения файла: {e}")
        sys.exit(1)
    
    # Создаём интерпретатор и выполняем код
    интерпретатор = РусКодИнтерпретатор()
    
    try:
        интерпретатор.выполнить(код)
    except Exception as e:
        print(f"Ошибка выполнения: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    главный()
