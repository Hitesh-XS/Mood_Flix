# 🎬 MoodFlix: AI-Driven Movie Recommendation Platform

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-6.0-092E20.svg)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-F7931E.svg)
![UI](https://img.shields.io/badge/UI-Tailwind%20CSS-38B2AC.svg)

MoodFlix is a secure, personalized web application that goes beyond generic "Top 10" lists. By leveraging Natural Language Processing (NLP) and a custom content-based filtering algorithm, the platform builds a unique "likeness matrix" for every user based on their individual rating history to deliver highly tailored movie recommendations.

---

## ✨ Key Features

* **🧠 Content-Based AI Engine:** Analyzes user ratings and processes movie genres/plot summaries using **TF-IDF Vectorization** and **Cosine Similarity** to instantly recommend mathematically matching films.
* **🔒 Secure User Vaults:** Fully gated platform. Users must authenticate to access their personalized dashboards, search engines, and rating histories (Session-based Auth via Django).
* **🎯 "Cold-Start" Fallback Engine:** If a brand-new user has no rating history, the engine intelligently falls back to global TMDB "Trending" metrics to ensure a populated, beautiful UI.
* **✨ Cinematic UI/UX:** A highly responsive, dark-mode frontend featuring glassmorphism, dynamic grids, and custom empty-state SVGs.
* **🔍 Global Search:** A fast, database-driven search bar for tracking down specific titles.

---

## 🛠️ Technology Stack

* **Backend:** Python, Django 6.0
* **Machine Learning:** Scikit-learn (TF-IDF, Cosine Similarity), Pandas, Pickle
* **Database:** SQLite (Development)
* **Frontend:** HTML5, Tailwind CSS (Utility-first styling)
* **Environment:** `python-dotenv` for API & Secret Key security

---

## 🚀 Local Installation & Setup

Want to run MoodFlix on your own machine? Follow these steps:

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/Niyantrak.git](https://github.com/yourusername/Niyantrak.git)
cd Niyantrak