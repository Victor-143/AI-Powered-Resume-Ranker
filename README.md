# 🧑‍💻 AI-Powered Resume Ranker  

An intelligent **Resume Ranking System** that evaluates resumes against job descriptions using **Natural Language Processing (NLP)** and **Machine Learning**. This tool helps recruiters and hiring managers shortlist the most relevant candidates efficiently.  

---

## 🚀 Features  
- 📄 **Resume Parsing** – Extracts text from PDF/DOCX resumes.  
- 📝 **Job Description Matching** – Matches resumes against job requirements.  
- 🎯 **Scoring Algorithm** – Assigns a relevance score to each resume.  
- ⚡ **Batch Processing** – Supports multiple resumes at once.  
- 🌐 **Web Interface** – Simple UI to upload resumes & job descriptions.  
- 📊 **Ranked Output** – Displays ranked candidates with scores.  

---

## 🛠️ Tech Stack  
- **Frontend:** HTML, CSS, Bootstrap (via Flask templates)  
- **Backend:** Python (Flask)  
- **NLP/ML:** scikit-learn, spaCy, NLTK  
- **File Handling:** PyPDF2, python-docx  
- **Others:** Jinja2 templates  

---

## 📂 Project Structure  

resume-ranker/
│── app.py # Flask main app
│── preprocess.py # Resume text preprocessing functions
│── scorer.py # Resume scoring logic
│── utils_pdf.py # PDF parsing utility
│── requirements.txt # Dependencies
│── templates/ # HTML templates
│── static/ # CSS, JS, images
│── sample_outputs/ # Example ranked results
│── README.md # Project documentation
│── .gitignore # Ignored files/folders

---

## ⚙️ Installation  

1️⃣ Clone the repository  
```bash
git clone https://github.com/Victor-143/AI-Powered-Resume-Ranker.git
cd AI-Powered-Resume-Ranker

2️⃣ Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # (Linux/Mac)
.venv\Scripts\activate      # (Windows)

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run the Flask app
python app.py

5️⃣ Open your browser and go to:
👉 http://127.0.0.1:5000/

🖥️ Usage

Upload resumes (PDF/DOCX).

Enter/paste the Job Description.

Click Rank Resumes.

Get ranked results with relevance scores.

📸 Screenshots

Add screenshots of your app UI here, e.g., upload page & results page

🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.
