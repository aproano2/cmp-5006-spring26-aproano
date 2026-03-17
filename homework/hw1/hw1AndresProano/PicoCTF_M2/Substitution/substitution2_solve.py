#!/usr/bin/env python3
import math
import random
import re
from collections import Counter

ALPHABET = "abcdefghijklmnopqrstuvwxyz"

def clean_letters(s: str) -> str:
    return "".join(ch for ch in s.lower() if ch.isalpha())

def build_ngram_model(training_text: str, n: int):
    """
    Devuelve (logp_dict, floor_logp) para n-gramas.
    Suavizado: cualquier n-gram no visto usa floor.
    """
    t = clean_letters(training_text)
    if len(t) < n:
        return {}, -10.0

    counts = Counter(t[i:i+n] for i in range(len(t) - n + 1))
    total = sum(counts.values())
    # floor pequeño pero no cero
    floor = math.log10(0.01 / total) if total > 0 else -10.0
    logp = {g: math.log10(c / total) for g, c in counts.items()} if total > 0 else {}
    return logp, floor

def score_ngram(text: str, logp, floor, n: int) -> float:
    t = clean_letters(text)
    if len(t) < n:
        return float("-inf")
    s = 0.0
    for i in range(len(t) - n + 1):
        g = t[i:i+n]
        s += logp.get(g, floor)
    return s

def extra_bonus(text: str) -> float:
    """
    Bonus suave para empujar hacia resultados útiles.
    No "resuelve por ti"; solo prioriza que aparezcan patrones esperados.
    """
    tl = text.lower()
    bonus = 0.0

    # Premia cosas típicas del inglés (muy suave)
    for w in ["the", "and", "that", "this", "with", "have", "you", "not", "for", "are"]:
        bonus += 2.0 * tl.count(w)

    # Premia tener llaves (bandera) y el formato picoCTF si aparece
    if "{" in text and "}" in text:
        bonus += 50.0
    if "picoctf{" in tl:
        bonus += 2000.0

    return bonus

def score_total(text: str, model2, floor2, model3, floor3, model4, floor4) -> float:
    """
    Score combinado. Pesos ajustados para texto sin espacios:
    - 4-grama manda, 3-grama ayuda, 2-grama estabiliza.
    """
    s4 = score_ngram(text, model4, floor4, 4)
    s3 = score_ngram(text, model3, floor3, 3)
    s2 = score_ngram(text, model2, floor2, 2)
    if any(v == float("-inf") for v in [s2, s3, s4]):
        return float("-inf")
    return (1.00 * s4) + (0.35 * s3) + (0.08 * s2) + extra_bonus(text)

def random_key():
    """
    key[i] = plain_letter asignada a la letra cifrada ALPHABET[i]
    (mapeo: cipher -> plain)
    """
    perm = list(ALPHABET)
    random.shuffle(perm)
    return perm

def decrypt(ciphertext: str, key) -> str:
    table = {ALPHABET[i]: key[i] for i in range(26)}
    out = []
    for ch in ciphertext:
        lo = ch.lower()
        if lo in table:
            p = table[lo]
            out.append(p.upper() if ch.isupper() else p)
        else:
            out.append(ch)
    return "".join(out)

def mutate_key_swap(key, locked=None):
    """
    Swap de dos posiciones (dos letras cifradas cambian sus asignaciones).
    locked: set de índices (0-25) que NO se pueden tocar.
    """
    locked = locked or set()
    candidates = [i for i in range(26) if i not in locked]
    if len(candidates) < 2:
        return key[:]
    a, b = random.sample(candidates, 2)
    k2 = key[:]
    k2[a], k2[b] = k2[b], k2[a]
    return k2

def find_best_braced_candidate(text: str):
    """
    Si no aparece picoCTF{...}, al menos extrae el mejor candidato {...}
    con caracteres típicos de flags.
    """
    # flags suelen ser alfanuméricas + underscore dentro de llaves
    m = re.findall(r"\{[A-Za-z0-9_]+\}", text)
    if not m:
        return None
    # elige el más largo como candidato
    return max(m, key=len)

def anneal(ciphertext: str, model2, floor2, model3, floor3, model4, floor4,
           restarts=80, steps=22000, T0=6.0, Tend=0.05, seed=None,
           lock_if_close=True):
    """
    Simulated annealing con reinicios.
    lock_if_close: si encuentra un candidato con {...} tipo flag, hace una fase final
    con menos temperatura para “pulir”.
    """
    if seed is not None:
        random.seed(seed)

    best_key = None
    best_score = float("-inf")
    best_plain = ""

    for r in range(restarts):
        key = random_key()
        plain = decrypt(ciphertext, key)
        cur_score = score_total(plain, model2, floor2, model3, floor3, model4, floor4)

        for i in range(steps):
            # temperatura lineal descendente
            t = T0 + (Tend - T0) * (i / steps)

            cand_key = mutate_key_swap(key)
            cand_plain = decrypt(ciphertext, cand_key)
            cand_score = score_total(cand_plain, model2, floor2, model3, floor3, model4, floor4)

            delta = cand_score - cur_score
            if delta > 0 or random.random() < math.exp(delta / max(t, 1e-6)):
                key, plain, cur_score = cand_key, cand_plain, cand_score

        if cur_score > best_score:
            best_key, best_score, best_plain = key, cur_score, plain

    # Fase de pulido si ya hay algo con formato de flag (ayuda mucho)
    if lock_if_close:
        cand = find_best_braced_candidate(best_plain)
        if cand:
            # “cooling” agresivo para refinar
            key = best_key[:]
            plain = best_plain
            cur_score = best_score
            for i in range(12000):
                t = 0.6  # baja temperatura constante
                cand_key = mutate_key_swap(key)
                cand_plain = decrypt(ciphertext, cand_key)
                cand_score = score_total(cand_plain, model2, floor2, model3, floor3, model4, floor4)
                delta = cand_score - cur_score
                if delta > 0 or random.random() < math.exp(delta / max(t, 1e-6)):
                    key, plain, cur_score = cand_key, cand_plain, cand_score
            if cur_score > best_score:
                best_key, best_score, best_plain = key, cur_score, plain

    return best_key, best_score, best_plain

def print_key_mapping(key):
    """
    Imprime tabla cipher->plain en formato legible para documentar.
    """
    cipher = ALPHABET
    plain = "".join(key)
    return (
        "Cipher: " + " ".join(cipher) + "\n"
        "Plain : " + " ".join(plain) + "\n"
    )

def main():
    import argparse
    ap = argparse.ArgumentParser(description="Solve monoalphabetic substitution locally using n-gram scoring + annealing.")
    ap.add_argument("-i", "--input", required=True, help="ciphertext file (message.txt)")
    ap.add_argument("-c", "--corpus", required=True, help="local corpus text file (e.g., en-the-little-prince.txt)")
    ap.add_argument("-o", "--output", default="decrypted.txt", help="save best plaintext here")
    ap.add_argument("--restarts", type=int, default=90, help="random restarts")
    ap.add_argument("--steps", type=int, default=24000, help="steps per restart")
    ap.add_argument("--seed", type=int, default=None, help="random seed for reproducibility")
    args = ap.parse_args()

    ciphertext = open(args.input, "r", encoding="utf-8").read().strip()
    corpus_text = open(args.corpus, "r", encoding="utf-8", errors="ignore").read()

    model2, floor2 = build_ngram_model(corpus_text, 2)
    model3, floor3 = build_ngram_model(corpus_text, 3)
    model4, floor4 = build_ngram_model(corpus_text, 4)

    key, sc, plain = anneal(
        ciphertext, model2, floor2, model3, floor3, model4, floor4,
        restarts=args.restarts, steps=args.steps, seed=args.seed
    )

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(plain + "\n\n")
        f.write(print_key_mapping(key))

    print("Best score:", sc)

    m = re.search(r"picoCTF\{[^}]+\}", plain)
    if m:
        print("FLAG FOUND:", m.group(0))
    else:
        cand = find_best_braced_candidate(plain)
        if cand:
            print("No picoCTF{...} yet. Best {...} candidate found:", cand)
        else:
            print("No braced candidate found. Try increasing --restarts/--steps.")

    print("\nKey mapping saved in decrypted.txt (bottom).")

if __name__ == "__main__":
    main()