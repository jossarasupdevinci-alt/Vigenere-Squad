import json
from pathlib import Path
from docx import Document
from docx.shared import Inches

doc = Document()
doc.add_heading("Vigenère-Squad : Système Multi-Agents Local pour la Cryptanalyse Classique", 0)
doc.add_paragraph("Rapport technique et expérimental — Architecture hybride déterministe et LLM locaux (Ollama)")

env = json.loads(Path("results/ENVIRONMENT.json").read_text(encoding="utf-8"))
metrics = json.loads(Path("results/metrics.json").read_text(encoding="utf-8"))

doc.add_heading("1. Contexte et Architecture Multi-Agents", level=1)
doc.add_paragraph(
    "Le projet Vigenère-Squad implémente une architecture multi-agents locale destinée à l'analyse et au déchiffrement "
    "de procédés cryptographiques classiques (César, Affine, Substitution monoalphabétique, Vigenère, Autoclave). "
    "Les calculs mathématiques et statistiques sont exécutés par des outils Python déterministes, tandis que les modèles "
    "locaux (Ollama) assurent le choix stratégique d'outils et la justification pédagogique."
)
doc.add_paragraph(
    "• ClassifierAgent : calcule l'indice de coïncidence (IC) et les fréquences.\n"
    "• CryptanalystAgent : sélectionne et exécute l'attaque appropriée via une liste fermée d'outils.\n"
    "• LinguistAgent : évalue la plausibilité linguistique (quadgrammes français) et déclenche une boucle de rejet/correction.\n"
    "• PedagogueAgent : rédige une explication étape par étape et génère un exercice similaire corrigé."
)

doc.add_heading("2. Environnement Expérimental et Reproductibilité", level=1)
doc.add_paragraph(
    f"Date de mesure : {metrics['date_mesure']} | OS : {env['os']} | "
    f"Python : {env['python']} | Processeur : {env['processeur']} | Corpus : {metrics['corpus_taille']} messages."
)
doc.add_paragraph(
    "La base de code est validée par 122 tests unitaires et tests de défaillance (pytest). "
    "Les prompts système sont versionnés dans prompts/ avec suivi dans CHANGELOG.md."
)

doc.add_heading("3. Preuve Expérimentale : Chiffre Autoclave vs Test de Kasiski", level=1)
ak = metrics["autoclave_vs_kasiski"]
doc.add_paragraph(
    f"Sur {ak['echantillons']} messages chiffrés par procédé Autoclave, le test de Kasiski obtient {ak['succes_kasiski_pct']} % "
    f"de réussite contre {ak['succes_attaque_autoclave_pct']} % pour l'attaque Autoclave dédiée."
)
t1 = doc.add_table(rows=3, cols=3)
t1.style = "Table Grid"
t1.rows[0].cells[0].text = "Méthode évaluée"
t1.rows[0].cells[1].text = "Échantillons"
t1.rows[0].cells[2].text = "Taux de réussite (%)"
t1.rows[1].cells[0].text = "Test de Kasiski seul"
t1.rows[1].cells[1].text = str(ak["echantillons"])
t1.rows[1].cells[2].text = f"{ak['succes_kasiski_pct']} %"
t1.rows[2].cells[0].text = "Attaque Autoclave dédiée"
t1.rows[2].cells[1].text = str(ak["echantillons"])
t1.rows[2].cells[2].text = f"{ak['succes_attaque_autoclave_pct']} %"

doc.add_heading("4. Étude d'Ablation (3 Configurations)", level=1)
t2 = doc.add_table(rows=4, cols=4)
t2.style = "Table Grid"
for idx, h in enumerate(["Configuration", "Modèle", "Taux clair exact (%)", "Temps moyen / msg (s)"]):
    t2.rows[0].cells[idx].text = h
for row_idx, (cfg_key, cfg_val) in enumerate(metrics["etude_ablation"].items(), 1):
    t2.rows[row_idx].cells[0].text = cfg_key
    t2.rows[row_idx].cells[1].text = str(cfg_val["modele"])
    t2.rows[row_idx].cells[2].text = f"{cfg_val['taux_clair_exact_moyenne_pct']} %"
    t2.rows[row_idx].cells[3].text = f"{cfg_val['temps_moyen_s']} s"

doc.add_heading("5. Étude de Robustesse", level=1)
t3 = doc.add_table(rows=4, cols=3)
t3.style = "Table Grid"
t3.rows[0].cells[0].text = "Scénario de dégradation"
t3.rows[0].cells[1].text = "Taux clair exact (%)"
t3.rows[0].cells[2].text = "Temps moyen (s)"
for r_idx, (rob_key, rob_val) in enumerate(metrics["robustesse"].items(), 1):
    t3.rows[r_idx].cells[0].text = rob_key
    t3.rows[r_idx].cells[1].text = f"{rob_val['taux_clair_exact_pct']} %"
    t3.rows[r_idx].cells[2].text = f"{rob_val['temps_moyen_par_chiffre_s']} s"

doc.add_heading("6. Validation Empirique de la Distance d'Unicité de Shannon", level=1)
doc.add_paragraph(
    "La distance d'unicité théorique U = (L * log2(26)) / 3,2 représente la borne inférieure d'information. "
    "En pratique, l'attaque statistique par colonnes exige 25 à 85 fois plus de caractères (180 à 500 lettres)."
)
fig_path = Path("results/figures/figure_shannon.png")
if fig_path.exists():
    doc.add_picture(str(fig_path), width=Inches(6.0))

t4 = doc.add_table(rows=len(metrics["shannon"]) + 1, cols=3)
t4.style = "Table Grid"
t4.rows[0].cells[0].text = "Longueur clé L"
t4.rows[0].cells[1].text = "Distance unicité théorique (car.)"
t4.rows[0].cells[2].text = "Seuil empirique >= 90 % (car.)"
for idx, pt in enumerate(metrics["shannon"], 1):
    t4.rows[idx].cells[0].text = str(pt["longueur_cle"])
    t4.rows[idx].cells[1].text = str(pt["distance_unicite_shannon"])
    t4.rows[idx].cells[2].text = str(pt["longueur_min_succes_90_pct"])

doc.add_heading("7. Analyse de Sécurité (STRIDE) et Limites", level=1)
doc.add_paragraph(
    "• Usurpation / Hallucination d'outils : rejet systématique hors de la liste fermée OUTILS_CRYPTANALYSTE.\n"
    "• Injection de prompt via texte chiffré : seuls des indicateurs numériques (IC, longueur) sont transmis au LLM.\n"
    "• Déni de service (boucles infinies) : bornage strict par max_iterations et max_retries.\n"
    "• Limites : dépendance à la langue française des quadgrammes, sensibilité aux textes courts et latence CPU des LLM locaux."
)

doc.save("RAPPORT_TECHNIQUE_VIGENERE_SQUAD.docx")
print("Rapport généré avec succès : RAPPORT_TECHNIQUE_VIGENERE_SQUAD.docx")