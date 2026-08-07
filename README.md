# Green Box Intel — AI Legal Document Intelligence Platform

Green Box Intel is an enterprise-grade, AI-powered B2B SaaS platform designed for legal teams and personal injury law firms. It automates the extraction, chronological organization, and billing analysis of large, multi-page medical injury records into concise, executive-level legal reports.

---

## 🌟 Key Features

* **Automated Medical Chronology Generation:** Aggregates multi-document medical records and organizes clinical events into a date-ordered timeline.
* **Smart Billing Ledger Extraction:** Identifies treatment costs, medical provider billing, and total damages automatically.
* **PII Anonymization & Shielding:** Masks sensitive personal health information (PHI) and personally identifiable information (PII) before sending data to external LLM providers.
* **Incremental Case Appending:** Allows lawyers to append supplemental medical records to an existing case, updating the master report dynamically via background tasks.
* **Export Options:** Generates formatted `.docx` reports and executive summaries directly for trial prep and demand letters.
* **Extra Features:** AI Chatbot available to interact with the report for obtaining specific information from the report.
* **Case File Organization** All the cases are well orgainized helping the lawyers to go thrtough past cases .

---

## 🛠️ Architecture & Tech Stack

### **Frontend**
* **Streamlit:** Interactive dashboard UI for legal document uploads, live quota tracking, and interactive report editing.

### **Backend & API**
* **FastAPI:** Asynchronous Python REST API handling file streams, background tasks, and authentication.
* **SQLAlchemy:** ORM for managing database operations and schema auto-generations.

### **Cloud Infrastructure & Security (AWS)**
* **AWS Textract:** Asynchronous OCR pipeline with forms/tables detection for dense legal PDFs.
* **AWS S3:** Secure cloud storage for raw document handling and processed text artifacts.
* **AWS RDS (PostgreSQL):** Relational database storing user profiles, usage quotas, and case metadata.

### **AI & NLP Pipeline**
* **Groq API / Llama 3.3 70B:** High-throughput LLM inference for report merging, chronology synthesis, and executive summaries.
(Strong Models will be used as per the client needs).
* **Microsoft Presidio:** Local PII/PHI detection and masking engine.

**Clone the repository:**

git clone [https://github.com/your-username/green-box-intel.git](https://github.com/cr0wn37/green-box-intel)
cd green-box-intel

**Set up a virtual environment:**

python -m venv venv
source venv/bin/activate  

**Install dependencies:**

pip install -r requirements.txt

**Running the Application**

uvicorn backend.main:app --reload --port 8000
python -m streamlit run frontend/main_entry.py
---

## 📁 Repository Structure

```text
GREEN_BOX_LEGAL/
├── backend/
│   ├── .env                 # required environment variables.
│   ├── approve_user.py      # Admin script to approve new user accounts
│   ├── aws_utils.py         # AWS S3 integration & Textract OCR pipeline
│   ├── database.py          # SQLAlchemy models & DatabaseManager class
│   ├── fix_columns.py       # Database schema column patch utility
│   ├── main.py              # FastAPI backend API entry point
│   ├── reset_db.py          # Database reset & table initialization script
│   └── requirements.txt     # Backend Python dependencies
├── frontend/
│   ├── .streamlit/          # Streamlit configuration & server settings
│   ├── assets/              # Logo, images, and custom CSS styles
│   ├── app.py               # Core application dashboard & case views
│   ├── landing_page.py      # Public landing page component
│   ├── login_page.py        # Authentication & user login interface
│   └── main_entry.py        # Streamlit main entry router
├── .gitignore               # Git ignored files & directories
├── CNAME                    # Custom domain configuration
├── index.html               # Landing page web entry point
├── README.md                # Project documentation
└── requirements.txt         # Global project dependencies