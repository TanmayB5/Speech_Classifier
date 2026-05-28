import re

# words that dont add meaning, strip them before embedding
FILLERS = {"um", "uh", "like", "okay", "please", "just", "so", "yeah", "yep", "hey"}

CONTRACTIONS = {
    "don't": "do not",
    "can't": "cannot",
    "i'm": "i am",
    "i've": "i have",
    "it's": "it is",
    "that's": "that is",
    "won't": "will not",
    "didn't": "did not",
    # TODO: add more if needed
}

def normalize_text(text):
    text = text.lower().strip()

    for c, expanded in CONTRACTIONS.items():
        text = text.replace(c, expanded)

    # remove punctuation
    text = re.sub(r"[^\w\s]", "", text)

    # handle repeated chars eg "staart" -> "staat" (not perfect but helps a bit)
    text = re.sub(r"(.)\1{2,}", r"\1\1", text)

    words = text.split()
    words = [w for w in words if w not in FILLERS]

    return " ".join(words).strip()
