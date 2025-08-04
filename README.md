# 🔐 Phishing URL Detection System | Network Security Project

An end-to-end Machine Learning system to detect phishing websites based on over 30 URL-based and HTML-based features. This project demonstrates a complete MLOps workflow from data processing to model deployment.

---

## 🚀 Project Highlights

- ✅ **30+ Engineered Features** extracted from URLs to detect phishing behavior
- ✅ **98% Accuracy** achieved using Random Forest (tuned) on labeled dataset
- ✅ Fully modular **ETL pipeline**: Data Ingestion → Validation → Transformation → Training
- ✅ **Web app deployment** with FastAPI + Streamlit on **AWS EC2**
- ✅ CI/CD with **GitHub Actions**, **Docker**, **MLflow**, **DVC**, and **S3** for artifact tracking
- ✅ **MongoDB Atlas** used for structured feature and logging storage
- ✅ Seamless **feature extraction**, **API serving**, and **browser-based testing**

---

## 🧠 Tech Stack

| Layer               | Tools/Technologies                                              |
|---------------------|------------------------------------------------------------------|
| Language            | Python                                                          |
| ML Libraries        | scikit-learn, pandas, numpy                                     |
| Deployment          | FastAPI, Streamlit, Docker, AWS EC2                            |
| MLOps Tools         | MLflow, DVC, GitHub Actions, AWS S3                            |
| Database            | MongoDB Atlas                                                   |
| CI/CD               | GitHub Actions + Docker                                         |

---

## 🗂️ Project Structure





---

## ⚙️ Pipeline Overview

### 1. **Data Ingestion**
- Reads raw data from CSV or S3
- Stores raw artifact using DVC

### 2. **Data Validation**
- Checks schema consistency
- Validates missing/null/unexpected values

### 3. **Data Transformation**
- Extracts 30+ handcrafted features
- Handles outliers, encodes categories

### 4. **Model Training**
- Trains multiple ML models (RF, DT, LR, XGBoost)
- Evaluates via accuracy, precision, recall
- Logs experiments using MLflow

### 5. **Prediction & Serving**
- FastAPI server serves predictions
- Feature extraction on-the-fly from user-input URL
- Streamlit provides interactive web interface

---

## 🖥️ Running the Project Locally

### 🔧 
```bash
git clone https://github.com/yourusername/phishing-detection.git
cd phishing-detection



python -m venv myenv
source myvenv/bin/activate  # On Windows: mvenv\Scripts\activate
pip install -r requirements.txt

uvicorn app:app --reload
streamlit run streamlit_app.py
docker build -t phishing-detector .
docker run -p 8000:8000 phishing-detector

🧪 Example URLs for Testing
Type	Example URLs
✅ Good	https://www.youtube.com
https://www.nytimes.com
❌ Phishing	http://198.51.100.23/login
http://paypal-login.com

🙌 Acknowledgements
Dataset: Phishing Websites Dataset - UCI ML Repo

Inspired by real-world phishing detection techniques and OWASP recommendations

📬 Contact
Ali Abdullah
📧 aliabdullah@example.com
🔗 LinkedIn • GitHub