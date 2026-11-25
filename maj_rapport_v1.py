import json
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

m = json.loads(Path("results/metrics.json").read_text(encoding="utf-8"))
e = json.loads(Path("results/ENVIRONMENT.json").read_text(encoding="utf-8"))

doc = Document()
style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(11)
style.paragraph_format.line_spacing = 1.35
style.paragraph_format.space_after = Pt(8)

# --- PAGE DE GARDE ---
doc.add_paragraph("\n\n")
t = doc.add_heading("RAPPORT TECHNIQUE — VIGENÈRE-SQUAD", 0)
t.alignment = WD_ALIGN_PARAGRAPH.CENTER
sub = doc.add_paragraph("Architecture Multi-Agents Locale avec Outils Déterministes pour la Cryptanalyse Classique")
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
doc.add_paragraph("\n\n")
meta = doc.add_paragraph(
    f"Version du projet : 1.0.0 (Consolidation finale)\n"
    f"Auteur : Jossara | Date de mesure : {m['date_mesure']}\n"
    f"Environnement : {e['os']} | Python {e['python']} | {e['processeur']}\n"
    f"Dépôt GitHub : https://github.com/jossarasupdevinci-alt/Vigenere-Squad\n"
    f"Page publique : https://jossarasupdevinci-alt.github.io/Vigenere-Squad/"
)
meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
doc.add_page_break()

# --- RÉSUMÉ BILINGUE (FRANÇAIS & ANGLAIS) ---
doc.add_heading("Résumé (Français)", level=1)
doc.add_paragraph(
    "Vigenère-Squad est un système multi-agents local en Python conçu pour automatiser, auditer et expliquer pédagogiquement "
    "la cryptanalyse des chiffrements classiques (César, affine, Vigenère, autoclave, substitution monoalphabétique et transposition) "
    "sur un ordinateur portable standard de 8 Go de mémoire vive sans carte graphique dédiée ni abonnement à des API cloud.\n"
    "L'architecture repose sur une séparation stricte entre les outils cryptographiques et statistiques déterministes (indice de coïncidence, "
    "analyse fréquentielle, test du chi-deux, méthode de Kasiski, estimation de Friedman, recuit simulé sur quadgrammes français et attaque "
    "séquentielle de l'autoclave, validés par 122 tests automatisés) et quatre agents spécialisés (Classifier, Cryptanalyst, Linguist, Pedagogue) "
    "pilotés localement via Ollama. Nos expériences sur un corpus reproductible de 150 messages français (graine 42) démontrent la supériorité "
    "de l'attaque dédiée sur l'autoclave (90,0 % contre 0,0 % pour Kasiski), quantifient l'impact de l'orchestration agentique par étude d'ablation "
    "et mesurent l'écart entre la distance d'unicité théorique de Shannon (4,41 à 14,69 caractères) et le seuil empirique de 90 % de réussite (180 à 500 caractères)."
)

doc.add_heading("Abstract (English)", level=1)
doc.add_paragraph(
    "Vigenère-Squad is a local Python multi-agent system designed to automate, audit, and pedagogically explain the cryptanalysis "
    "of classical ciphers (Caesar, affine, Vigenère, autokey, monoalphabetic substitution, and transposition) on a standard 8 GB RAM laptop "
    "without GPU acceleration or commercial cloud APIs.\n"
    "The architecture enforces a strict separation between deterministic cryptographic/statistical tools (index of coincidence, frequency analysis, "
    "chi-squared test, Kasiski examination, Friedman estimation, simulated annealing over French quadgrams, and sequential autokey recovery, verified "
    "by 122 automated tests) and four specialized agents (Classifier, Cryptanalyst, Linguist, Pedagogue) powered locally via Ollama. Benchmarks on a "
    "reproducible 150-message French corpus (seed 42) demonstrate the effectiveness of dedicated autokey recovery (90.0% vs. 0.0% for Kasiski), "
    "quantify agentic overhead through an ablation study, and measure the gap between Shannon's theoretical unicity distance (4.41 to 14.69 characters) "
    "and the empirical 90% recovery threshold (180 to 500 characters)."
)
doc.add_page_break()

# --- REPRISE ET ACTUALISATION DES SECTIONS DU RAPPORT ---
md_lines = Path("RAPPORT_TECHNIQUE.md").read_text(encoding="utf-8").splitlines()
for line in md_lines:
    s = line.strip()
    if not s or s.startswith("RAPPORT TECHNIQUE") or s.startswith("**Version") or s.startswith("**Date") or s.startswith("**Langage") or s.startswith("**Dépôt") or s == "---":
        continue
    if s.startswith("12. Évaluation expérimentale"):
        break
    if s[0].isdigit() and ". " in s[:5]:
        if s.startswith(("4. ", "7. ", "10. ")):
            doc.add_page_break()
        doc.add_heading(s, level=1)
    elif s.startswith(("6.1.", "6.2.", "6.3.")):
        doc.add_heading(s, level=2)
    else:
        doc.add_paragraph(s)

# --- NOUVELLE SECTION 12 : RÉSULTATS EXPÉRIMENTAUX CONSOLIDÉS (v1.0.0) ---
doc.add_page_break()
doc.add_heading("12. Résultats Expérimentaux Consolidés (v1.0.0)", level=1)

ak = m["autoclave_vs_kasiski"]
doc.add_heading("12.1. Validation de l'attaque dédiée contre le chiffrement Autokey", level=2)
doc.add_paragraph(
    f"Conformément aux travaux identifiés dans la version 0.1.0, une attaque spécifique à l'autoclave (recherche d'amorce et propagation "
    f"séquentielle guidée par les quadgrammes) a été implémentée et évaluée sur {ak['echantillons']} cryptogrammes autoclaves :\n"
    f"• Test de Kasiski + attaque Vigenère classique : {ak['succes_kasiski_pct']} % de réussite.\n"
    f"• Attaque dédiée Autoclave : {ak['succes_attaque_autoclave_pct']} % de récupération exacte du texte clair."
)

doc.add_heading("12.2. Étude d'ablation : Impact des agents et des modèles locaux", level=2)
t_ab = doc.add_table(rows=4, cols=4)
t_ab.style = "Table Grid"
for i, h in enumerate(["Configuration", "Modèle LLM", "Clair exact (%)", "Temps moyen / msg (s)"]):
    t_ab.rows[0].cells[i].text = h
for idx, (k, v) in enumerate(m["etude_ablation"].items(), 1):
    t_ab.rows[idx].cells[0].text = k
    t_ab.rows[idx].cells[1].text = str(v["modele"])
    t_ab.rows[idx].cells[2].text = f"{v['taux_clair_exact_moyenne_pct']} %"
    t_ab.rows[idx].cells[3].text = f"{v['temps_moyen_s']} s"
doc.add_paragraph(
    "Analyse : Les outils déterministes garantissent la même précision cryptographique (16,67 % sur l'échantillon mixte), tandis que les "
    "modèles locaux Ollama ajoutent un surcoût de ~9,5 à 10,3 s par message pour assurer le routage explicable, la gestion des rejets et "
    "l'explication pédagogique."
)

doc.add_heading("12.3. Étude de robustesse aux perturbations", level=2)
t_rob = doc.add_table(rows=4, cols=3)
t_rob.style = "Table Grid"
for i, h in enumerate(["Condition expérimentale", "Clair exact (%)", "Temps moyen (s)"]):
    t_rob.rows[0].cells[i].text = h
for idx, (k, v) in enumerate(m["robustesse"].items(), 1):
    t_rob.rows[idx].cells[0].text = k
    t_rob.rows[idx].cells[1].text = f"{v['taux_clair_exact_pct']} %"
    t_rob.rows[idx].cells[2].text = f"{v['temps_moyen_par_chiffre_s']} s"
doc.add_paragraph(
    "La suppression des espaces maintient 50,0 % de réussite exacte, tandis que 5 % de bruit ou un changement de langue (anglais avec modèle "
    "de quadgrammes français) ramènent l'égalité stricte caractère par caractère à 0,0 %."
)

doc.add_heading("12.4. Distance d'unicité de Shannon : théorie vs pratique", level=2)
doc.add_paragraph(
    "La distance d'unicité de Shannon U = H(K)/D prédit la longueur théorique minimale d'un cryptogramme pour identifier de manière unique "
    "une clé de longueur L. La figure et le tableau ci-dessous comparent cette borne théorique à la longueur minimale observée empiriquement "
    "pour atteindre au moins 90 % de déchiffrement exact :"
)
if Path("results/figures/figure_shannon.png").exists():
    doc.add_picture("results/figures/figure_shannon.png", width=Inches(5.8))

t_sh = doc.add_table(rows=len(m["shannon"]) + 1, cols=3)
t_sh.style = "Table Grid"
for i, h in enumerate(["Longueur de clé L", "Distance théorique U (car.)", "Longueur min empirique >= 90 % (car.)"]):
    t_sh.rows[0].cells[i].text = h
for idx, r in enumerate(m["shannon"], 1):
    t_sh.rows[idx].cells[0].text = str(r["longueur_cle"])
    t_sh.rows[idx].cells[1].text = str(r["distance_unicite_shannon"])
    t_sh.rows[idx].cells[2].text = str(r["longueur_min_succes_90_pct"])

# --- SECTION 13 : CONCLUSION & RÉFÉRENCES ---
doc.add_page_break()
doc.add_heading("13. Conclusion et Références", level=1)
doc.add_paragraph(
    "Vigenère-Squad démontre la pertinence d'une architecture hybride associant des outils cryptographiques déterministes et auditables "
    "à des agents locaux spécialisés. L'ensemble des objectifs fixés (attaque dédiée Autokey à 90 %, étude d'ablation, robustesse, validation "
    "empirique de la distance d'unicité de Shannon et 122 tests automatisés) est consolidé et vérifiable via SHA256SUMS et AUDIT.md.\n\n"
    "Références :\n"
    "• Shannon, C. E. (1949). Communication Theory of Secrecy Systems. Bell System Technical Journal.\n"
    "• Kasiski, F. W. (1863). Die Geheimschriften und die Dechiffrir-Kunst.\n"
    "• Friedman, W. F. (1922). The Index of Coincidence and Its Applications in Cryptography."
)

Path("docs").mkdir(exist_ok=True)
doc.save("docs/rapport.docx")
print("OK : docs/rapport.docx v1.0.0 genere avec succes !")