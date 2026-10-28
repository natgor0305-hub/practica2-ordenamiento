# Lee results.csv y genera tablas (Markdown) y graficas (PNG)
import csv, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
rows = list(csv.DictReader(open("results.csv")))
for lang in ("cpp", "py"):
    R = [r for r in rows if r["lenguaje"] == lang]
    print(f"\n### {lang}: tiempo (s) / memoria pico (MB)\n\n| Algoritmo | n | Tiempo (s) | Memoria (MB) |\n|---|---|---|---|")
    for r in R: print(f"| {r['algoritmo']} | {int(r['n']):,} | {r['tiempo_s']} | {r['memoria_MB']} |")
    for key, name in (("tiempo_s", "Tiempo (s)"), ("memoria_MB", "Memoria pico (MB)")):
        plt.figure(figsize=(7, 4.5))
        for algo in sorted({r["algoritmo"] for r in R}):
            pts = [(int(r["n"]), float(r[key])) for r in R if r["algoritmo"] == algo and r["tiempo_s"].replace('.', '', 1).isdigit()]
            if pts: plt.plot(*zip(*pts), marker="o", label=algo)
        plt.xscale("log"); plt.yscale("log"); plt.xlabel("n"); plt.ylabel(name); plt.title(f"{name} ({lang})")
        plt.grid(True, which="both", alpha=.3); plt.legend(); plt.tight_layout(); plt.savefig(f"{key}_{lang}.png", dpi=150); plt.close()
