"""Midterm 1 solver: computes every number from my_data/ (Parts 1, 2, 3).
Usage: python solve.py (after make_my_data.py) standard library only.
Parses-DATA.md with regexes, so it adapts to whatever numbers the exam code produces."""
import csv, math, re, sys
from pathlib import Path

D = Path(__file__).parent / "my_data"
md = (D / "DATA.md").read_text(encoding="utf-8")
Z = 1.96

def num(s): return float(s.replace(",", "").replace(" ", ""))
def grab(pat, text=md):
    m = re.search(pat, text, re.S)
    if not m: sys.exit(f"pattern not found: {pat}")
    return num(m.group(1))

def wilson(h, n):
    p = h / n
    den = 1 + Z**2 / n
    c = (p + Z**2 / (2 * n)) / den
    hw = Z * math.sqrt(p * (1 - p) / n + Z**2 / (4 * n**2)) / den
    return p, c - hw, c + hw

def section(title):
    i = md.index(title)
    j = md.find("\n### ", i + len(title))
    return md[i: j if j > 0 else len(md)]

print("Fingerprint:", re.search(r"Fingerprint: `(\w+)`", md).group(1))

# ---------------- Part 1 ----------------
rows = list(csv.DictReader(open(D / "retrieval_ranks.csv", encoding="utf-8")))
N = len(rows)
print(f"\n=== PART 1 (n={N}) ===\n1a")
print("| config | recall@1 | recall@3 | recall@5 | MRR@10 |")
for cfg in "AB":
    r = [int(x[f"rank_{cfg}"]) for x in rows]
    rec = [sum(v <= k for v in r) / N for k in (1, 3, 5)]
    mrr = sum(1 / v for v in r if v <= 10) / N
    print(f"| {cfg} | " + " | ".join(f"{x:.3f}" for x in rec) + f" | {mrr:.3f} |")

langs = []
traffic = {}
for m in re.finditer(r"^\| (\w\w) \| (\d+) % \| (\d+) \| (\d+) \| (\d+) \| (\d+) \|", md, re.M):
    L = m.group(1); langs.append(L)
    traffic[L] = dict(share=int(m.group(2)) / 100, q=int(m.group(3)), ans=int(m.group(4)),
                      A=int(m.group(5)), B=int(m.group(6)))
req = grab(r"Requests per day: \*\*([\d,]+)\*\*")
sysp = grab(r"System prompt: \*\*([\d,]+)\*\*")
pin = grab(r"Price: \*\*\$([\d.]+)\*\* per million input")
pout = grab(r"\*\*\$([\d.]+)\*\* per million output tokens\.\n- Annual budget")
budget = grab(r"Annual budget.*?\*\*\$([\d,]+)\*\*")

print("\n1b + 1c   (budget = %.0f)" % budget)
print("| candidate | recall@k | lower | upper | annual cost | within budget |")
for cfg in "AB":
    for k in (3, 5):
        h = sum(int(x[f"rank_{cfg}"]) <= k for x in rows)
        p, lo, hi = wilson(h, N)
        cost = 0
        for L in langs:
            t = traffic[L]
            cin = sysp + t["q"] + k * t[cfg]
            cost += t["share"] * (cin * pin + t["ans"] * pout) / 1e6
        annual = cost * req * 365
        print(f"| {cfg}, k={k} | {p:.3f} ({h}/{N}) | {lo:.3f} | {hi:.3f} | {annual:,.0f} | {'yes' if annual <= budget else 'NO'} |")

print("\nPer-language recall@k (for 1d):")
for cfg in "AB":
    for k in (3, 5):
        parts = []
        for L in langs:
            sub = [x for x in rows if x["lang"] == L]
            h = sum(int(x[f"rank_{cfg}"]) <= k for x in sub)
            p, lo, hi = wilson(h, len(sub))
            parts.append(f"{L} {h}/{len(sub)}={p:.2f} [{lo:.2f},{hi:.2f}]")
        print(f"  {cfg},k={k}: " + "  ".join(parts))

# ---------------- Part 2 ----------------
print("\n=== PART 2 ===")
docs = list(csv.DictReader(open(D / "doc_results.csv", encoding="utf-8")))
pages = grab(r"Volume: \*\*([\d,]+)\*\* scanned pages")
pd_share = grab(r"In \*\*([\d.]+) %\*\* of them") / 100
w = grab(r"Page image: \*\*(\d+) ×")
hgt = grab(r"× (\d+)\*\* pixels")
out_tok = grab(r"returns about \*\*(\d+)\*\* output tokens")
h_in = grab(r"Pipeline H price: \*\*\$([\d.]+)\*\*")
h_out = grab(r"Pipeline H price:.*?per million input tokens, \*\*\$([\d.]+)\*\*")
srv = grab(r"one server costs \*\*\$([\d,]+)\*\*")
cap = grab(r"handles up to \*\*([\d,]+)\*\* pages")

img_tok = math.ceil(w / 28) * math.ceil(hgt / 28)
costH = pages * 365 * (img_tok * h_in + out_tok * h_out) / 1e6
costL = math.ceil(pages / cap) * srv * 12
cost = {"H": costH, "L": costL}
print(f"image tokens/page = {math.ceil(w/28)} x {math.ceil(hgt/28)} = {img_tok}")
print("| pipeline | overall accuracy | weakest cell | accuracy there | lower | upper | annual cost |")
for P in ("H", "L"):
    sub = [x for x in docs if x["pipeline"] == P]
    n = sum(int(x["n_docs"]) for x in sub); c = sum(int(x["n_correct"]) for x in sub)
    worst = min(sub, key=lambda x: int(x["n_correct"]) / int(x["n_docs"]))
    p, lo, hi = wilson(int(worst["n_correct"]), int(worst["n_docs"]))
    print(f"| {P} | {c/n:.3f} ({c}/{n}) | {worst['lang']}, {worst['condition']} | {p:.3f} ({worst['n_correct']}/{worst['n_docs']}) | {lo:.3f} | {hi:.3f} | {cost[P]:,.0f} |")
print(f"Personal-data pages/year abroad under H: {pages*365*pd_share:,.0f}")
print("\nAll cells with Wilson CI:")
for x in docs:
    p, lo, hi = wilson(int(x["n_correct"]), int(x["n_docs"]))
    print(f"  {x['pipeline']} {x['lang']} {x['condition']:9} {x['n_correct']}/{x['n_docs']} = {p:.3f} [{lo:.3f}, {hi:.3f}]")

# ---------------- Part 3 ----------------
print("\n=== PART 3 ===")
q = section("### Q1")
r = {m.group(1): tuple(map(int, m.group(2, 3, 4)))
     for m in re.finditer(r"^\| (EN|RU|KK) \| (\d+) \| (\d+) \| (\d+) \|", q, re.M)}
rc, rb, rt = (r["KK"][i] / r["EN"][i] for i in range(3))
print(f"Q1: chars {rc:.2f}, bytes {rb:.2f}, tokens {rt:.2f} -> token/byte = {rt/rb:.2f}")

q = section("### Q2")
size = grab(r"chunk size to \*\*(\d+) tokens", q)
frac = grab(r"starts (\d+) % of the way", q) / 100
en_rate = grab(r"produced chunks of (\d+)", q) / 256
pos = size * en_rate * frac
limit = grab(r"reads at most (\d+)", q)
print(f"Q2: EN chunk = {size}*{en_rate:.4f} = {size*en_rate:.1f} e5 tokens; start = {pos:.1f} -> {round(pos)} (limit {limit:.0f}; truncated: {pos >= limit})")

q = section("### Q3")
T = grab(r"temperature T = (\d+(?:\.\d+)?)", q)
sc = [(m.group(1), float(m.group(2))) for m in re.finditer(r"^\| (\w+) \| ([\d.]+) \|", q, re.M)]
ex = [math.exp(s / T) for _, s in sc]; Zs = sum(ex)
print("Q3: " + ", ".join(f"{t} {e/Zs*100:.1f}%" for (t, _), e in zip(sc, ex)))
ex1 = [math.exp(s) for _, s in sc]; Z1 = sum(ex1)
print("    (T=1 for comparison: " + ", ".join(f"{t} {e/Z1*100:.1f}%" for (t, _), e in zip(sc, ex1)) + ")")

q = section("### Q4")
mods = {m.group(1): tuple(map(int, m.group(2, 3, 4)))
        for m in re.finditer(r"^\| Model (\w) \| (\d+) \| (\d+) \| (\d+) \|", q, re.M)}
pen = {k: c - wr for k, (c, wr, _) in mods.items()}
print(f"Q4: penalised X={pen['X']}, Y={pen['Y']} -> Y-X = {pen['Y']-pen['X']} (leaderboard: X={mods['X'][0]}, Y={mods['Y'][0]})")

q = section("### Q5")
t = grab(r"adds \*\*(\d+) new tokens", q); n = int(grab(r"has \*\*(\d+) turns", q))
print(f"Q5: {t:.0f} * {n}*{n+1}/2 = {t*n*(n+1)/2:,.0f} tokens; first message paid {n} times")