# Practica 2 - Complejidad de ordenamiento (Python 3)
# Uso: python3 sorting.py <bubble|merge|tree|heap|counting> <n>
import sys, time, random, resource
M = 1_000_000

def bubble(a):
    n = len(a)
    for i in range(n - 1):
        sw = False
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]; sw = True
        if not sw: break
    return a

def merge(a):                       # mergesort ascendente iterativo con buffer auxiliar
    n = len(a); src, dst = a, [0.0] * n; w = 1
    while w < n:
        for l in range(0, n, 2 * w):
            m, r = min(l + w, n), min(l + 2 * w, n); i, j, k = l, m, l
            while i < m and j < r:
                if src[i] <= src[j]: dst[k] = src[i]; i += 1
                else:                dst[k] = src[j]; j += 1
                k += 1
            while i < m: dst[k] = src[i]; i += 1; k += 1
            while j < r: dst[k] = src[j]; j += 1; k += 1
        src, dst = dst, src; w *= 2
    return src

def tree(a):                        # BST sin balancear, todo iterativo
    n = len(a)
    if n < 2: return a
    val = a[:]; L = [-1] * n; R = [-1] * n
    for i in range(1, n):
        x = val[i]; cur = 0
        while True:
            if x < val[cur]:
                if L[cur] < 0: L[cur] = i; break
                cur = L[cur]
            else:
                if R[cur] < 0: R[cur] = i; break
                cur = R[cur]
    out, st, cur = [], [], 0
    while cur != -1 or st:
        while cur != -1: st.append(cur); cur = L[cur]
        cur = st.pop(); out.append(val[cur]); cur = R[cur]
    return out

def _sift(a, n, i):
    x = a[i]
    while True:
        c = 2 * i + 1
        if c >= n: break
        if c + 1 < n and a[c + 1] > a[c]: c += 1
        if a[c] <= x: break
        a[i] = a[c]; i = c
    a[i] = x

def heap(a):
    n = len(a)
    for i in range(n // 2 - 1, -1, -1): _sift(a, n, i)
    for e in range(n - 1, 0, -1):
        a[0], a[e] = a[e], a[0]; _sift(a, e, 0)
    return a

def counting(a):                    # llave entera = round(x*100)
    c = [0] * M
    for x in a: c[int(round(x * 100))] += 1
    out = []
    for v in range(M):
        if c[v]: out.extend([v / 100.0] * c[v])
    return out

ALGS = dict(bubble=bubble, merge=merge, tree=tree, heap=heap, counting=counting)
if __name__ == "__main__":
    algo, n = sys.argv[1], int(sys.argv[2])
    rng = random.Random(42)
    a = [rng.randrange(M) / 100.0 for _ in range(n)]
    t0 = time.perf_counter(); a = ALGS[algo](a); s = time.perf_counter() - t0
    ok = all(a[i] <= a[i + 1] for i in range(len(a) - 1))
    print(f"py,{algo},{n},{s:.4f},{resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024:.1f},{int(ok)}")
