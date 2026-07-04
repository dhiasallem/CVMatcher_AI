import re


def normalize_words(text: str) -> set:
    """
    Transforme un texte en un ensemble de mots uniques, en minuscules,
    sans ponctuation.

    Args:
        text: texte à transformer.

    Returns:
        Un set (ensemble) de mots uniques.
    """
    text = text.lower()
    # Garde uniquement les lettres, chiffres et espaces (enlève la ponctuation)
    text = re.sub(r'[^a-zà-ÿ0-9\s]', ' ', text)
    words = text.split()
    return set(words)


def basic_score(cv_text: str, offre_text: str) -> float:
    """
    Calcule un score de similarité basique entre un CV et une offre
    d'emploi, basé sur le nombre de mots en commun.

    Args:
        cv_text: texte du CV (déjà nettoyé).
        offre_text: texte de l'offre d'emploi.

    Returns:
        Un score entre 0 et 1 (0 = aucun mot en commun, 1 = mots identiques).
    """
    cv_words = normalize_words(cv_text)
    offre_words = normalize_words(offre_text)

    if not offre_words:
        return 0.0

    mots_communs = cv_words.intersection(offre_words)

    # Le score = proportion des mots de l'offre qui se retrouvent dans le CV
    score = len(mots_communs) / len(offre_words)
    return round(score, 2)

from sentence_transformers import SentenceTransformer, util

# Le modèle est chargé une seule fois, en dehors des fonctions,
# car le chargement est lent (quelques secondes)
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')


def semantic_score(cv_text: str, offre_text: str) -> float:
    """
    Calcule un score de similarité sémantique entre un CV et une offre
    d'emploi, en utilisant des embeddings (le modèle comprend le sens,
    pas juste les mots exacts).

    Args:
        cv_text: texte du CV.
        offre_text: texte de l'offre d'emploi.

    Returns:
        Un score entre 0 et 1 (0 = aucun rapport, 1 = sens identique).
    """
    # Transforme chaque texte en vecteur numérique (embedding)
    embedding_cv = model.encode(cv_text, convert_to_tensor=True)
    embedding_offre = model.encode(offre_text, convert_to_tensor=True)

    # Calcule la similarité cosinus entre les deux vecteurs
    similarite = util.cos_sim(embedding_cv, embedding_offre)

    # Le résultat est une matrice 1x1, on extrait juste le nombre
    score = similarite.item()
    return round(score, 2)
if __name__ == "__main__":
    cv_exemple = """
    Jean Dupont
    Développeur Web
    Expérience : 3 ans chez WebCorp en tant que développeur front-end
    Compétences : HTML, CSS, JavaScript, Python, React
    """

    offre_exemple = """
    Recherche développeur front-end expérimenté.
    Compétences requises : JavaScript, React, HTML, CSS.
    Une expérience en Python est un plus.
    """

    score_basique = basic_score(cv_exemple, offre_exemple)
    print(f"Score basique (mots-clés) : {score_basique * 100:.0f}%")

    score_semantique = semantic_score(cv_exemple, offre_exemple)
    print(f"Score sémantique (embeddings) : {score_semantique * 100:.0f}%")