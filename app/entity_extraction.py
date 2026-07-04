import spacy
from spacy.matcher import PhraseMatcher
from skills_list import SKILLS
nlp = spacy.load("fr_core_news_sm")


def build_matcher() -> PhraseMatcher:
    """
    Construit un PhraseMatcher spaCy à partir de la liste de compétences.
    attr="LOWER" permet de matcher peu importe la casse
    (ex: "Python", "PYTHON", "python" sont tous détectés).
    """
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    patterns = [nlp.make_doc(skill) for skill in SKILLS]
    matcher.add("SKILL", patterns)
    return matcher


matcher = build_matcher()


def extract_skills(text: str) -> list[str]:
    """
    Extrait les compétences reconnues dans un texte.

    Args:
        text: texte du CV ou de l'offre.

    Returns:
        Liste triée des compétences trouvées (sans doublons).
    """
    doc = nlp(text)
    matches = matcher(doc)

    found = set()
    for match_id, start, end in matches:
        span = doc[start:end]
        found.add(span.text.lower())

    return sorted(found)


def compare_skills(cv_skills: list[str], offre_skills: list[str]) -> tuple[list[str], list[str]]:
    """
    Compare les compétences du CV à celles de l'offre.

    Returns:
        (compétences_communes, compétences_manquantes)
    """
    cv_set = set(cv_skills)
    offre_set = set(offre_skills)

    communes = sorted(cv_set & offre_set)
    manquantes = sorted(offre_set - cv_set)

    return communes, manquantes


import os
from extractor import extract_text, clean_text

if __name__ == "__main__":
    dossier = "data/sample_cvs"
    fichiers_pdf = [f for f in os.listdir(dossier) if f.endswith(".pdf")]

    if not fichiers_pdf:
        print(f"Aucun fichier PDF trouvé dans {dossier}/")
    else:
        sample_path = os.path.join(dossier, fichiers_pdf[0])
        raw_text = extract_text(sample_path)
        cv_texte = clean_text(raw_text)

        offre_exemple = """
        Recherche développeur front-end expérimenté.
        Compétences requises : JavaScript, React, HTML, CSS, TypeScript, Docker.
        Une expérience en Python est un plus.
        """

        cv_skills = extract_skills(cv_texte)
        offre_skills = extract_skills(offre_exemple)

        print("Compétences détectées dans le CV :", cv_skills)
        print("Compétences détectées dans l'offre :", offre_skills)

        communes, manquantes = compare_skills(cv_skills, offre_skills)
        print("\n✅ Compétences en commun :", communes)
        print("❌ Compétences manquantes :", manquantes)