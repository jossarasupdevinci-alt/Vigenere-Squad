import json
import math
import platform
import random
import statistics
import time
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt

from agents.orchestrator import Orchestrator
from scripts.chiffrement_vigenere import chiffrer_vigenere
from scripts.attaque_autoclave import attaquer_autoclave
from scripts.attaque_vigenere import attaquer_vigenere
from scripts.kasiski import analyser_kasiski
from scripts.score_quadgrammes import charger_modele


def nettoyer(texte: str) -> str:
    return "".join(c for c in texte.upper() if "A" <= c <= "Z")


def evaluer_echantillon(messages: list[dict], model_name: str | None, label: str = "") -> dict:
    orch = Orchestrator(model_name=model_name, max_iterations=2)
    succes = 0
    iterations_totales = 0
    durees = []

    for idx, msg in enumerate(messages, 1):
        print(f"   [{label}] message {idx}/{len(messages)}...", end="\r", flush=True)
        t0 = time.perf_counter()
        state = orch.run(msg["texte_chiffre"])
        dt = time.perf_counter() - t0
        durees.append(dt)
        iterations_totales += state.iteration_count
        if state.plaintext and nettoyer(state.plaintext) == nettoyer(msg["texte_clair"]):
            succes += 1

    print(f"   [{label}] terminé : {succes}/{len(messages)} succès (moy. {statistics.mean(durees):.2f}s/msg)      ")
    n = max(len(messages), 1)
    return {
        "taux_clair_exact_pct": round(100.0 * succes / n, 2),
        "iterations_moyennes": round(iterations_totales / n, 3),
        "temps_moyen_par_chiffre_s": round(statistics.mean(durees), 4),
    }


def main(mode_rapide: bool = False):
    print("=== Démarrage de la campagne expérimentale Vigenere-Squad ===", flush=True)
    ref_path = Path("data/corpus_genere/reference_privee.json")
    corpus = json.loads(ref_path.read_text(encoding="utf-8"))
    modele_quad = charger_modele()

    # 1. Preuve expérimentale Autoclave vs Kasiski
    print("\n[1/4] Test Autoclave vs Kasiski...", flush=True)
    autoclaves = [m for m in corpus if m["methode"] == "autoclave"][:10]
    kasiski_ok = 0
    autoclave_ok = 0
    for idx, m in enumerate(autoclaves, 1):
        print(f"   Autoclave {idx}/{len(autoclaves)}...", end="\r", flush=True)
        res_k = analyser_kasiski(m["texte_chiffre"])
        long_k = res_k[2] if isinstance(res_k, tuple) else None
        if long_k == len(m["cle"]):
            kasiski_ok += 1
        res_a = attaquer_autoclave(m["texte_chiffre"], modele_quad)
        if nettoyer(res_a["texte_clair"]) == nettoyer(m["texte_clair"]):
            autoclave_ok += 1
    print(f"   Kasiski : {kasiski_ok}/{len(autoclaves)} | Attaque Autoclave : {autoclave_ok}/{len(autoclaves)}      ")

    # 2. Étude d'ablation : 3 configurations
    print("\n[2/4] Étude d'ablation (3 configurations)...", flush=True)
    # En mode rapide, on prend 6 messages variés (1 par méthode) et 1 répétition
    if mode_rapide:
        par_methode = {}
        for m in corpus:
            if m["methode"] not in par_methode:
                par_methode[m["methode"]] = m
        sous_ensemble = list(par_methode.values())
        repetitions = 1
    else:
        sous_ensemble = corpus[:24]
        repetitions = 3

    configs = {
        "a_sans_llm_deterministe": None,
        "b_llm_8go_llama3_2_3b": "llama3.2:3b",
        "c_llm_leger_qwen3_0_6b": "qwen3:0.6b",
    }

    ablation = {}
    for nom_cfg, modele_llm in configs.items():
        runs = [
            evaluer_echantillon(sous_ensemble, modele_llm, label=f"{nom_cfg} run {r+1}/{repetitions}")
            for r in range(repetitions)
        ]
        taux = [r["taux_clair_exact_pct"] for r in runs]
        iters = [r["iterations_moyennes"] for r in runs]
        temps = [r["temps_moyen_par_chiffre_s"] for r in runs]
        ablation[nom_cfg] = {
            "modele": modele_llm or "aucun (heuristique)",
            "repetitions": repetitions,
            "taux_clair_exact_moyenne_pct": round(statistics.mean(taux), 2),
            "taux_clair_exact_ecart_type": round(statistics.stdev(taux), 2) if len(taux) > 1 else 0.0,
            "iterations_moyennes": round(statistics.mean(iters), 3),
            "temps_moyen_s": round(statistics.mean(temps), 4),
            "runs": runs,
        }

    # 3. Robustesse
    print("\n[3/4] Tests de robustesse (sans espaces, 5% fautes, anglais)...", flush=True)
    rng = random.Random(42)
    echantillon_rob = [m for m in corpus if m["methode"] in ("cesar", "vigenere")][:10]
    sans_espaces = [{**m, "texte_chiffre": nettoyer(m["texte_chiffre"])} for m in echantillon_rob]

    avec_fautes = []
    for m in echantillon_rob:
        chars = list(m["texte_chiffre"])
        for i in range(len(chars)):
            if "A" <= chars[i] <= "Z" and rng.random() < 0.05:
                chars[i] = chr(((ord(chars[i]) - ord("A") + 1) % 26) + ord("A"))
        avec_fautes.append({**m, "texte_chiffre": "".join(chars)})

    anglais_texte = (
        "CRYPTOGRAPHY IS THE PRACTICE AND STUDY OF TECHNIQUES FOR SECURE "
        "COMMUNICATION IN THE PRESENCE OF ADVERSARIAL BEHAVIOR AND CLASSICAL "
        "CIPHERS DEMONSTRATE FREQUENCY ANALYSIS CLEARLY"
    )
    corpus_en = [
        {"texte_clair": anglais_texte, "texte_chiffre": chiffrer_vigenere(anglais_texte, "KEY")}
        for _ in range(3)
    ]

    robustesse = {
        "sans_espaces_ni_ponctuation": evaluer_echantillon(sans_espaces, None, "sans_espaces"),
        "avec_5pct_fautes": evaluer_echantillon(avec_fautes, None, "5pct_fautes"),
        "corpus_anglais": evaluer_echantillon(corpus_en, None, "anglais"),
    }

    # 4. Figure de Shannon
    print("\n[4/4] Génération de la figure de Shannon...", flush=True)
    texte_base = Path("data/corpus_francais.txt").read_text(encoding="utf-8")
    texte_base = nettoyer(texte_base)[:3000]
    cles_test = ["CLE", "TEST", "CRYPT", "SECRET", "BONJOUR", "VIGENERE", "ANALYSEUR", "ALGORITHME"]
    longueurs_test = [30, 50, 80, 120, 180, 250, 350, 500]

    points_shannon = []
    for cle in cles_test:
        L = len(cle)
        longueur_min_90 = longueurs_test[-1]
        for N in longueurs_test:
            succes_N = 0
            essais = 5 if mode_rapide else 10
            for k in range(essais):
                extrait = texte_base[k * 50 : k * 50 + N]
                chiffre = chiffrer_vigenere(extrait, cle)
                res = attaquer_vigenere(chiffre, modele_quad)
                if nettoyer(res["texte_clair"]) == extrait:
                    succes_N += 1
            if (succes_N / essais) >= 0.90:
                longueur_min_90 = N
                break
        distance_unicite = round((L * math.log2(26)) / 3.2, 2)
        points_shannon.append({
            "longueur_cle": L,
            "longueur_min_succes_90_pct": longueur_min_90,
            "distance_unicite_shannon": distance_unicite,
        })
        print(f"   Clé L={L} -> N_min={longueur_min_90} (Shannon={distance_unicite})", flush=True)

    plt.figure(figsize=(8, 5))
    xs = [p["longueur_cle"] for p in points_shannon]
    ys_emp = [p["longueur_min_succes_90_pct"] for p in points_shannon]
    ys_th = [p["distance_unicite_shannon"] for p in points_shannon]
    plt.plot(xs, ys_emp, marker="o", label="Longueur minimale empirique (succès >= 90 %)")
    plt.plot(xs, ys_th, linestyle="--", marker="s", label="Distance d'unicité théorique de Shannon (français)")
    plt.xlabel("Longueur de la clé L (caractères)")
    plt.ylabel("Longueur minimale du texte chiffré N (caractères)")
    plt.title("Vigenère-Squad : Seuil expérimental de déchiffrement vs Distance d'unicité de Shannon")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig("results/figures/figure_shannon.png", dpi=150)
    plt.close()

    env_info = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "os": platform.platform(),
        "python": platform.python_version(),
        "processeur": platform.processor(),
    }
    Path("results/ENVIRONMENT.json").write_text(json.dumps(env_info, indent=2), encoding="utf-8")

    metrics = {
        "date_mesure": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "corpus_taille": len(corpus),
        "autoclave_vs_kasiski": {
            "echantillons": len(autoclaves),
            "succes_kasiski_pct": round(100.0 * kasiski_ok / max(len(autoclaves), 1), 2),
            "succes_attaque_autoclave_pct": round(100.0 * autoclave_ok / max(len(autoclaves), 1), 2),
        },
        "etude_ablation": ablation,
        "robustesse": robustesse,
        "shannon": points_shannon,
    }
    Path("results/metrics.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")
    Path("metrics.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")
    print("\n=== Expérimentations terminées avec succès ! Résultats dans results/metrics.json ===", flush=True)


if __name__ == "__main__":
    import sys
    main(mode_rapide="--small" in sys.argv)
