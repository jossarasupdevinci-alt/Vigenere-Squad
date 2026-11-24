import string
from scripts.chiffrement_autoclave import dechiffrer_autoclave
from scripts.indice_coincidence import calculer_indice_coincidence
from scripts.score_quadgrammes import calculer_score_moyen


def estimer_longueur_cle_autoclave(texte_chiffre: str, max_len: int = 12) -> list[tuple[int, float]]:
    lettres = [c for c in texte_chiffre.upper() if "A" <= c <= "Z"]
    scores = []

    for longueur in range(3, max_len + 1):
        if len(lettres) <= longueur + 10:
            continue

        differences = "".join(
            chr(((ord(lettres[i]) - ord(lettres[i - longueur])) % 26) + ord("A"))
            for i in range(longueur, len(lettres))
        )
        ic = calculer_indice_coincidence(differences)
        scores.append((longueur, ic))

    return sorted(scores, key=lambda x: x[1], reverse=True)


def attaquer_autoclave(texte_chiffre: str, modele: dict, max_len: int = 12) -> dict:
    estimations = estimer_longueur_cle_autoclave(texte_chiffre, max_len=max_len)
    longueurs_candidates = [longueur for longueur, _ in estimations[:3]]
    if not longueurs_candidates:
        longueurs_candidates = list(range(3, max_len + 1))

    meilleur_score = float("-inf")
    meilleure_cle = ""
    meilleur_clair = ""

    for longueur in longueurs_candidates:
        cle = ["A"] * longueur

        for _ in range(3):
            for pos in range(longueur):
                meilleure_lettre = cle[pos]
                score_local = float("-inf")

                for lettre in string.ascii_uppercase:
                    cle[pos] = lettre
                    candidat = dechiffrer_autoclave(texte_chiffre, "".join(cle))
                    score = calculer_score_moyen(candidat, modele)

                    if score > score_local:
                        score_local = score
                        meilleure_lettre = lettre

                cle[pos] = meilleure_lettre

        cle_candidate = "".join(cle)
        clair_candidat = dechiffrer_autoclave(texte_chiffre, cle_candidate)
        score_final = calculer_score_moyen(clair_candidat, modele)

        if score_final > meilleur_score:
            meilleur_score = score_final
            meilleure_cle = cle_candidate
            meilleur_clair = clair_candidat

    return {
        "cle": meilleure_cle,
        "longueur_cle": len(meilleure_cle),
        "texte_clair": meilleur_clair,
        "score": meilleur_score,
        "estimations_ic_diff": estimations,
    }
