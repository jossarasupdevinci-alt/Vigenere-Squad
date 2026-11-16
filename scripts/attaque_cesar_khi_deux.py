from scripts.force_brute_cesar import force_brute_cesar
from scripts.khi_deux import calculer_khi_deux
from scripts.analyse_linguistique import analyser_langue


def classer_resultats(message):
    resultats = force_brute_cesar(message)
    classement = []

    for cle, texte in resultats.items():
        score_khi = calculer_khi_deux(texte)
        score_langue = analyser_langue(texte)

        # Score combiné : le Khi-deux est normalisé
        # pour éviter qu'il domine le score linguistique.
        score_final = score_langue - (score_khi / 1000)

        classement.append(
            (score_final, cle, texte, score_khi, score_langue)
        )

    return sorted(classement, reverse=True)


if __name__ == "__main__":
    message = "ERQMRXU"

    classement = classer_resultats(message)

    print("Analyse du message :", message)
    print("\nLes 3 meilleures propositions :")

    for score, cle, texte, khi, langue in classement[:3]:
        print(
            f"Cle {cle} | Texte : {texte} | "
            f"Khi-deux : {khi:.2f} | "
            f"Langue : {langue:.2f} | "
            f"Score final : {score:.3f}"
        )
