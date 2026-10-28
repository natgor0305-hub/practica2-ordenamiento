# Práctica 2 – Complejidad de ordenamiento (ADA, 3BV1)
Alumnos: Melo Cruz Leonardo Galdino, González Ramírez Ángeles Nataly · Profesor: Andrés García Floriano

Algoritmos: Bubble sort, Mergesort, Tree sort (BST), Heapsort, Counting sort. Lenguajes: C++17 y Python 3.

## Uso
    g++ -O2 -std=c++17 -o sorting sorting.cpp
    python3 run_benchmarks.py 1800     # genera results.csv
    python3 make_report.py             # tablas + PNG

## Datos
Reales con 2 decimales en [0, 9999.99], semilla fija (42). Counting sort usa llave entera round(x*100) (rango 10^6).
Tiempo = solo el ordenamiento; memoria = pico RSS del proceso (incluye el arreglo de entrada).

## Contenido
- `sorting.cpp`, `sorting.py`: implementaciones de los 5 algoritmos.
- `run_benchmarks.py`: ejecuta los experimentos (límite de tiempo por corrida, omite tamaños que no caben en RAM) y genera `results.csv`.
- `make_report.py`: genera tablas (Markdown) y gráficas PNG a partir de `results.csv`.
- `results.csv`, `tablas.md`, `*.png`: resultados y gráficas.
- `Reporte_Practica2.pdf` / `.docx`: reporte escrito.
