from __future__ import annotations
import io
import uuid
from datetime import datetime
from typing import List
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
import pandas as pd
from utils_pdf import extract_text_from_pdf
from preprocess import preprocess
from scorer import ResumeDoc, rank_resumes

ALLOWED_EXT = {"pdf"}

app = Flask(__name__)
app.secret_key = "change-me"  # set via env var in production
app.config["REPORTS"] = {}    # token -> csv bytes

def allowed(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/rank")
def rank():
    jd_text = (request.form.get("jd_text") or "").strip()
    extra_keywords = (request.form.get("extra_keywords") or "").strip()
    alpha = float(request.form.get("alpha") or 0.7)
    files = request.files.getlist("resumes")

    if not jd_text:
        flash("Please paste a Job Description (JD).")
        return redirect(url_for("index"))
    if not files or all(f.filename == "" for f in files):
        flash("Please upload at least one PDF resume.")
        return redirect(url_for("index"))

    resumes: List[ResumeDoc] = []
    for f in files:
        if f and allowed(f.filename):
            fname = secure_filename(f.filename)
            pdf_bytes = f.read()
            raw = extract_text_from_pdf(pdf_bytes)
            pre = preprocess(raw)
            resumes.append(ResumeDoc(filename=fname, raw_text=raw, preprocessed=pre))
        else:
            flash(f"Skipping unsupported file: {f.filename}")

    if not resumes:
        flash("No valid PDF resumes were uploaded.")
        return redirect(url_for("index"))

    df = rank_resumes(resumes, jd_text, extra_keywords=extra_keywords, alpha=alpha)

    # build CSV in-memory and cache with a token
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    token = uuid.uuid4().hex
    app.config["REPORTS"][token] = csv_bytes

    return render_template(
        "results.html",
        results=df.to_dict(orient="records"),
        token=token,
        jd_preview=jd_text[:400] + ("..." if len(jd_text) > 400 else ""),
        extra_keywords=extra_keywords,
        alpha=alpha
    )

@app.get("/download/<token>")
def download(token: str):
    csv_bytes = app.config["REPORTS"].get(token)
    if not csv_bytes:
        flash("Report expired. Please re-run the ranking.")
        return redirect(url_for("index"))
    return send_file(
        io.BytesIO(csv_bytes),
        mimetype="text/csv",
        as_attachment=True,
        download_name=f"resume_ranks_{token[:8]}.csv"
    )

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
