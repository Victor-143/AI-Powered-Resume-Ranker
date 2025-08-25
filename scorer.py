from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from preprocess import preprocess, tokenize_set

@dataclass
class ResumeDoc:
    filename: str
    raw_text: str
    preprocessed: str

def build_corpus(resumes: List[ResumeDoc], jd_text: str) -> List[str]:
    return [preprocess(jd_text)] + [r.preprocessed for r in resumes]

def vectorize_and_score(resumes: List[ResumeDoc], jd_text: str) -> Tuple[np.ndarray, TfidfVectorizer]:
    corpus = build_corpus(resumes, jd_text)
    vectorizer = TfidfVectorizer(max_features=5000)
    tfidf = vectorizer.fit_transform(corpus)
    sims = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()
    return sims, vectorizer

def keyword_boost(resumes: List[ResumeDoc], jd_text: str, extra_keywords: str = "") -> np.ndarray:
    jd_tokens = tokenize_set(jd_text)
    extra_tokens = tokenize_set(extra_keywords)
    keywords = sorted((jd_tokens | extra_tokens))
    if not keywords:
        return np.zeros(len(resumes))
    scores = []
    for r in resumes:
        tokens = set(r.preprocessed.split())
        matched = sum(1 for k in keywords if k in tokens)
        scores.append(matched / len(keywords))
    return np.array(scores, dtype=float)

def final_scores(cosine_sims: np.ndarray, kw_scores: np.ndarray, alpha: float = 0.7) -> np.ndarray:
    alpha = float(np.clip(alpha, 0.0, 1.0))
    return alpha * cosine_sims + (1.0 - alpha) * kw_scores

def rank_resumes(resumes: List[ResumeDoc], jd_text: str, extra_keywords: str = "", alpha: float = 0.7) -> pd.DataFrame:
    sims, _ = vectorize_and_score(resumes, jd_text)
    kw = keyword_boost(resumes, jd_text, extra_keywords)
    scores = final_scores(sims, kw, alpha=alpha)
    df = pd.DataFrame({
        "filename": [r.filename for r in resumes],
        "cosine_similarity": sims,
        "keyword_score": kw,
        "final_score": scores,
    })
    df.sort_values(by="final_score", ascending=False, inplace=True, kind="mergesort")
    df.reset_index(drop=True, inplace=True)
    df.index = df.index + 1
    df["rank"] = df.index
    return df[["rank", "filename", "final_score", "cosine_similarity", "keyword_score"]]
