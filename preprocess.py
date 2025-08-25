from __future__ import annotations
import re
import spacy

try:
    nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])
except OSError as e:
    raise RuntimeError(
        "SpaCy model 'en_core_web_sm' not found. Run: python -m spacy download en_core_web_sm"
    ) from e

_PUNCT_RE = re.compile(r"[^a-zA-Z0-9\s]")

def normalize_text(text: str) -> str:
    text = text or ""
    text = text.lower()
    text = _PUNCT_RE.sub(" ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def spacy_lemmatize(text: str) -> str:
    if not text:
        return ""
    doc = nlp(text)
    kept = []
    for tok in doc:
        if tok.is_stop or tok.is_space or tok.like_num:
            continue
        lemma = tok.lemma_.strip()
        if len(lemma) < 2:
            continue
        kept.append(lemma)
    return " ".join(kept)

def preprocess(text: str) -> str:
    return spacy_lemmatize(normalize_text(text))

def tokenize_set(text: str) -> set[str]:
    return set(preprocess(text).split())
