import os
import re
import pdfplumber


def extract_text(pdf_path: str) -> str:
    
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def clean_text(text: str) -> str:
    
    # Remplace les espaces multiples (y compris tabulations) par un seul espace
    text = re.sub(r'[ \t]+', ' ', text)

    # Supprime les espaces en début et fin de chaque ligne
    lines = [line.strip() for line in text.split('\n')]

    # Supprime les lignes complètement vides
    lines = [line for line in lines if line]

    # Recolle le tout avec un seul saut de ligne entre chaque ligne
    return '\n'.join(lines)


if __name__ == "__main__":
    dossier = "data/sample_cvs"
    fichiers_pdf = [f for f in os.listdir(dossier) if f.endswith(".pdf")]

    if not fichiers_pdf:
        print(f"Aucun fichier PDF trouvé dans {dossier}/")
        print("Ajoute un CV en PDF dans ce dossier avant de relancer.")
    else:
        sample_path = os.path.join(dossier, fichiers_pdf[0])
        print(f"Fichier trouvé : {sample_path}")

        raw_text = extract_text(sample_path)
        cleaned = clean_text(raw_text)

        print("--- Texte brut ---")
        print(raw_text)
        print(f"\n--- Longueur brute : {len(raw_text)} caractères ---\n")

        print("--- Texte nettoyé ---")
        print(cleaned)
        print(f"\n--- Longueur nettoyée : {len(cleaned)} caractères ---")