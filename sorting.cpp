// Practica 2 - Complejidad de ordenamiento (C++17)
// Uso: ./sorting <bubble|merge|tree|heap|counting> <n>
#include <bits/stdc++.h>
#include <sys/resource.h>
using namespace std;
using Clock = chrono::steady_clock;
static const uint32_t M = 1000000;      // valores reales con 2 decimales: 0.00 .. 9999.99
static const uint32_t NIL = UINT32_MAX;

void bubble(vector<double>& a) {
    size_t n = a.size();
    for (size_t i = 0; i + 1 < n; i++) {
        bool sw = false;
        for (size_t j = 0; j + 1 < n - i; j++)
            if (a[j] > a[j + 1]) { swap(a[j], a[j + 1]); sw = true; }
        if (!sw) break;
    }
}
void merge_rec(double* a, double* t, size_t l, size_t r) {
    if (r - l < 2) return;
    size_t m = l + (r - l) / 2;
    merge_rec(a, t, l, m); merge_rec(a, t, m, r);
    size_t i = l, j = m, k = l;
    while (i < m && j < r) t[k++] = (a[i] <= a[j]) ? a[i++] : a[j++];
    while (i < m) t[k++] = a[i++];
    while (j < r) t[k++] = a[j++];
    memcpy(a + l, t + l, (r - l) * sizeof(double));
}
void mergesort_(vector<double>& a) {
    vector<double> t(a.size());
    merge_rec(a.data(), t.data(), 0, a.size());
}
struct Node { double v; uint32_t l, r; };
void treesort(vector<double>& a) {            // BST sin balancear; insercion e inorden iterativos
    size_t n = a.size(); if (n < 2) return;
    vector<Node> t; t.reserve(n);
    for (size_t i = 0; i < n; i++) {
        t.push_back({a[i], NIL, NIL});
        if (i == 0) continue;
        uint32_t cur = 0;
        for (;;) {
            if (a[i] < t[cur].v) { if (t[cur].l == NIL) { t[cur].l = i; break; } cur = t[cur].l; }
            else                 { if (t[cur].r == NIL) { t[cur].r = i; break; } cur = t[cur].r; }
        }
    }
    vector<uint32_t> st; size_t k = 0; uint32_t cur = 0;
    while (cur != NIL || !st.empty()) {
        while (cur != NIL) { st.push_back(cur); cur = t[cur].l; }
        cur = st.back(); st.pop_back();
        a[k++] = t[cur].v; cur = t[cur].r;
    }
}
static void sift(double* a, size_t n, size_t i) {
    double x = a[i];
    for (;;) {
        size_t c = 2 * i + 1; if (c >= n) break;
        if (c + 1 < n && a[c + 1] > a[c]) c++;
        if (a[c] <= x) break;
        a[i] = a[c]; i = c;
    }
    a[i] = x;
}
void heapsort_(vector<double>& a) {
    size_t n = a.size();
    for (size_t i = n / 2; i-- > 0;) sift(a.data(), n, i);
    for (size_t e = n; e-- > 1;) { swap(a[0], a[e]); sift(a.data(), e, 0); }
}
void counting(vector<double>& a) {            // llave entera = round(x*100)
    vector<uint32_t> c(M, 0);
    for (double x : a) c[(size_t)llround(x * 100)]++;
    size_t k = 0;
    for (size_t v = 0; v < M; v++)
        for (uint32_t q = c[v]; q--;) a[k++] = v / 100.0;
}
int main(int argc, char** argv) {
    if (argc < 3) { fprintf(stderr, "uso: %s algo n\n", argv[0]); return 1; }
    string algo = argv[1]; size_t n = strtoull(argv[2], 0, 10);
    vector<double> a(n);
    mt19937_64 rng(42);
    for (size_t i = 0; i < n; i++) a[i] = (rng() % M) / 100.0;
    auto t0 = Clock::now();
    if      (algo == "bubble")   bubble(a);
    else if (algo == "merge")    mergesort_(a);
    else if (algo == "tree")     treesort(a);
    else if (algo == "heap")     heapsort_(a);
    else if (algo == "counting") counting(a);
    else { fprintf(stderr, "algoritmo desconocido\n"); return 1; }
    double s = chrono::duration<double>(Clock::now() - t0).count();
    bool ok = is_sorted(a.begin(), a.end());
    struct rusage ru; getrusage(RUSAGE_SELF, &ru);
    printf("cpp,%s,%zu,%.4f,%.1f,%d\n", algo.c_str(), n, s, ru.ru_maxrss / 1024.0, (int)ok);
}
