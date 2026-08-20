#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Математическая библиотека для РусКод.
Содержит более 100 математических функций.
"""

import math
from functools import reduce

функции = {}

# === Базовые математические функции ===
функции['плюс'] = lambda *args: sum(args) if args else 0
функции['минус'] = lambda a, b=0: a - b
функции['умножить'] = lambda *args: eval('*'.join(map(str, args))) if args else 1
функции['разделить'] = lambda a, b: a / b if b != 0 else 0
функции['степень'] = lambda a, b: a ** b
функции['корень'] = lambda x, n=2: x ** (1/n) if x >= 0 else complex(x ** (1/n))
функции['модуль'] = lambda x: abs(x)
функции['округлить'] = lambda x, n=0: round(x, int(n))
функции['округлить_вверх'] = lambda x: math.ceil(x)
функции['округлить_вниз'] = lambda x: math.floor(x)
функции['целое'] = lambda x: int(x)
функции['дробное'] = lambda x: float(x)

# === Тригонометрические функции ===
функции['синус'] = lambda x: math.sin(math.radians(x))
функции['косинус'] = lambda x: math.cos(math.radians(x))
функции['тангенс'] = lambda x: math.tan(math.radians(x))
функции['арксинус'] = lambda x: math.degrees(math.asin(x))
функции['арккосинус'] = lambda x: math.degrees(math.acos(x))
функции['арктангенс'] = lambda x: math.degrees(math.atan(x))
функции['гиперболический_синус'] = lambda x: math.sinh(x)
функции['гиперболический_косинус'] = lambda x: math.cosh(x)
функции['гиперболический_тангенс'] = lambda x: math.tanh(x)

# === Логарифмические функции ===
функции['логарифм'] = lambda x, base=math.e: math.log(x, base)
функции['натуральный_логарифм'] = lambda x: math.log(x)
функции['десятичный_логарифм'] = lambda x: math.log10(x)
функции['двоичный_логарифм'] = lambda x: math.log2(x)

# === Факториал и комбинаторика ===
функции['факториал'] = lambda n: math.factorial(int(n))
функции['перестановки'] = lambda n, k: math.perm(int(n), int(k))
функции['сочетания'] = lambda n, k: math.comb(int(n), int(k))
функции['размещения'] = lambda n, k: math.perm(int(n), int(k))

# === НОД и НОК ===
функции['нод'] = lambda a, b: math.gcd(int(a), int(b))
функции['нок'] = lambda a, b: abs(a * b) // math.gcd(int(a), int(b)) if a and b else 0

# === Простые числа ===
def _простое_ли(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

функции['простое_ли'] = lambda n: _простое_ли(int(n))
функции['следующее_простое'] = lambda n: next(i for i in range(int(n)+1, 10**6) if _простое_ли(i))
функции['предыдущее_простое'] = lambda n: next(i for i in range(int(n)-1, 1, -1) if _простое_ли(i))

def _простые_до(n):
    return [i for i in range(2, int(n)+1) if _простое_ли(i)]

функции['простые_до'] = lambda n: _простые_до(n)
функции['количество_простых'] = lambda n: len(_простые_до(n))

# === Числа Фибоначчи ===
def _фибоначчи(n):
    if n <= 0:
        return 0
    if n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, int(n)+1):
        a, b = b, a + b
    return b

def _фибоначчи_список(n):
    if n <= 0:
        return []
    if n == 1:
        return [0]
    seq = [0, 1]
    for i in range(2, int(n)):
        seq.append(seq[-1] + seq[-2])
    return seq

функции['фибоначчи'] = lambda n: _фибоначчи(int(n))
функции['фибоначчи_список'] = lambda n: _фибоначчи_список(int(n))

# === Статистические функции ===
функции['среднее'] = lambda lst: sum(lst) / len(lst) if lst else 0
функции['медиана'] = lambda lst: sorted(lst)[len(lst)//2] if lst else 0
функции['мода'] = lambda lst: max(set(lst), key=lst.count) if lst else None
функции['дисперсия'] = lambda lst: sum((x - sum(lst)/len(lst))**2 for x in lst) / len(lst) if lst else 0
функции['стандартное_отклонение'] = lambda lst: math.sqrt(функции['дисперсия'](lst))
функции['минимум'] = lambda *args: min(args) if args else 0
функции['максимум'] = lambda *args: max(args) if args else 0
функции['сумма'] = lambda lst: sum(lst)
функции['произведение'] = lambda lst: reduce(lambda x, y: x*y, lst, 1) if lst else 1

# === Случайные числа ===
import random
функции['случайное'] = lambda a=0, b=1: random.uniform(a, b)
функции['случайное_целое'] = lambda a, b: random.randint(int(a), int(b))
функции['случайный_выбор'] = lambda lst: random.choice(lst)
функции['случайная_выборка'] = lambda lst, k: random.sample(lst, min(int(k), len(lst)))
функции['перемешать'] = lambda lst: random.shuffle(lst) or lst

# === Константы ===
функции['пи'] = lambda: math.pi
функции['е'] = lambda: math.e
функции['тау'] = lambda: math.tau
функции['золотое_сечение'] = lambda: (1 + math.sqrt(5)) / 2

# === Преобразование углов ===
функции['в_радианы'] = lambda deg: math.radians(deg)
функции['в_градусы'] = lambda rad: math.degrees(rad)

# === Гипотенуза и расстояния ===
функции['гипотенуза'] = lambda a, b: math.hypot(a, b)
функции['расстояние'] = lambda x1, y1, x2, y2: math.hypot(x2-x1, y2-y1)
функции['расстояние_3d'] = lambda x1, y1, z1, x2, y2, z2: math.sqrt((x2-x1)**2 + **(y2-y1)2 + (z2-z1)**2)

# === Делители ===
def _делители(n):
    n = int(n)
    дел = set()
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            дел.add(i)
            дел.add(n // i)
    return sorted(дел)

функции['делители'] = lambda n: _делители(n)
функции['количество_делителей'] = lambda n: len(_делители(n))
функции['сумма_делителей'] = lambda n: sum(_делители(n))

# === Совершенные числа ===
def _совершенное_ли(n):
    n = int(n)
    if n < 2:
        return False
    return sum(_делители(n)) - n == n

функции['совершенное_ли'] = lambda n: _совершенное_ли(n)

# === Модулярная арифметика ===
функции['модуль_число'] = lambda a, b: a % b
функции['модулярная_степень'] = lambda base, exp, mod: pow(int(base), int(exp), int(mod))
функции['обратный_элемент'] = lambda a, m: pow(int(a), -1, int(m))

# === Биномиальное распределение ===
функции['биномиальный_коэффициент'] = lambda n, k: math.comb(int(n), int(k))

# === Проверка на чётность ===
функции['чётное_ли'] = lambda n: int(n) % 2 == 0
функции['нечётное_ли'] = lambda n: int(n) % 2 != 0

# === Знак числа ===
функции['знак'] = lambda x: 1 if x > 0 else (-1 if x < 0 else 0)

# === Ограничение диапазона ===
функции['ограничить'] = lambda x, low, high: max(low, min(high, x))

# === Линейная интерполяция ===
функции['лерп'] = lambda a, b, t: a + (b - a) * t

# === Возведение в квадрат и куб ===
функции['квадрат'] = lambda x: x ** 2
функции['куб'] = lambda x: x ** 3

# === Средние значения ===
функции['среднее_геометрическое'] = lambda lst: reduce(lambda x, y: x*y, lst, 1) ** (1/len(lst)) if lst else 0
функции['среднее_гармоническое'] = lambda lst: len(lst) / sum(1/x for x in lst) if lst else 0

# === Римские цифры ===
def _в_римское(n):
    val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syms = ['M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I']
    n = int(n)
    рим = ''
    i = 0
    while n > 0:
        for _ in range(n // val[i]):
            рим += syms[i]
            n -= val[i]
        i += 1
    return рим

функции['в_римское'] = lambda n: _в_римское(int(n))
