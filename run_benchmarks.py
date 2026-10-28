# Ejecuta todos los experimentos y guarda results.csv
# Uso: python3 run_benchmarks.py [timeout_segundos=1800]
import subprocess, sys, csv, os
TIMEOUT = int(sys.argv[1]) if len(sys.argv) > 1 else 1800
SIZES = [10**5, 10**6, 10**7, 10**8, 10**9]
ALGOS = ["bubble", "merge", "tree", "heap", "counting"]
CMDS = {"cpp": ["./sorting"], "py": [sys.executable, "sorting.py"]}
BYTES = {"bubble": 8, "merge": 16, "tree": 8 + 16 + 4, "heap": 8, "counting": 8}   # bytes/elemento (C++)
def avail_mb():
    for l in open("/proc/meminfo"):
        if l.startswith("MemAvailable"): return int(l.split()[1]) / 1024
rows = []
for lang in CMDS:
    for algo in ALGOS:
        stop = None                               # si un tamano falla, los mayores tambien
        for n in SIZES:
            if stop:
                rows.append([lang, algo, n, stop, "", ""]); print(rows[-1]); continue
            mult = 1 if lang == "cpp" else 4          # Python usa ~4x+ mas memoria
            if BYTES[algo] * n * mult / 2**20 > 0.9 * avail_mb():
                res = [lang, algo, n, "SIN_RAM", "", ""]
            else:
                try:
                    p = subprocess.run(CMDS[lang] + [algo, str(n)], capture_output=True, text=True, timeout=TIMEOUT)
                    res = p.stdout.strip().split(",") if p.returncode == 0 else [lang, algo, n, "ERROR", "", ""]
                except subprocess.TimeoutExpired:
                    res = [lang, algo, n, "TIMEOUT", "", ""]
            print(res, flush=True); rows.append(res)
            if res[3] in ("TIMEOUT", "SIN_RAM", "ERROR"): stop = res[3]
with open("results.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["lenguaje", "algoritmo", "n", "tiempo_s", "memoria_MB", "ordenado"]); w.writerows(rows)
