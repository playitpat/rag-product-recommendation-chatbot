# Danone AI Consumer Assistant (RAG + Insights)

A sophisticated prototype of an **AI-powered consumer assistant** tailored for Danone Japan. This project demonstrates the intersection of conversational AI, Retrieval-Augmented Generation (RAG), and real-time marketing analytics.

---

## 🌟 Overview
This solution transforms standard consumer inquiries into actionable business intelligence. By leveraging RAG and structured insight extraction, it provides brand-safe interactions while feeding a live analytics dashboard.

### Core Value Proposition
* **Conversational Excellence:** Answers health and product questions with brand-compliant accuracy.
* **Smart Recommendations:** Contextually suggests products like *Danone Bio* or *Oikos*.
* **Insight Engine:** Automatically extracts consumer needs, intents, and innovation signals.
* **Data-Driven Innovation:** Empowers marketing teams with a lightweight analytics dashboard.

---

## ✨ Key Features

### 1. AI Consumer Assistant
* Natural language processing for fluid interactions.
* Product recommendations based on user goals (e.g., protein intake, digestion).
* **Compliance-First:** Non-medical, brand-safe tone of voice using soft claims.



### 2. RAG (Retrieval-Augmented Generation)
* **Knowledge Base:** Curated product data sourced from local files.
* **Accuracy:** Dramatically reduces hallucination by grounding responses in verified text.

### 3. Insight Extraction Layer
Every interaction is decomposed into structured data points:
* **Consumer Needs:** (e.g., Digestion, Muscle Recovery)
* **Intent:** (e.g., Purchase intent, General curiosity)
* **Context:** Sentiment, Persona, and Usage occasion.
* **Innovation Signals:** Identifies flavor requests and unmet product needs.

### 4. Consumer Insights Dashboard
* Visualizes real-time trends from user interactions.
* Identifies emerging needs and supports R&D/Marketing decision-making.



---

## 🏗 Architecture
The system follows a modular pipeline for scalability:

**User** → **Streamlit UI** → **RAG (ChromaDB)** → **OpenAI API** → **Insight Extraction** → **CSV/Log Storage** → **Analytics Dashboard**

---

## 📂 Project Structure
```text
├── app.py                      # Main Streamlit application
├── data/                       # Raw product knowledge (txt files)
│   ├── bio.txt
│   └── oikos.txt
├── chroma_db/                  # Vector database storage
├── consumer_insights_log.csv   # Structured conversation logs
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (API Keys)
└── README.md                   # Documentation
```

---

## 🚀 Setup Instructions

### 1. Clone the Repository
Bash
`git clone <your-repo-url>
cd <repo-name>`
### 2. Install Dependencies
Bash
`pip install -r requirements.txt`
### 3. Configuration
Create a .env file in the project root and add your credentials:

`OPENAI_API_KEY=your_api_key_here`
### 4. Populate Knowledge Base
Add .txt files to the data/ folder. These files are indexed by the RAG layer to ensure the assistant provides accurate product information.

### 5. Launch the Application
Bash
`streamlit run app.py`

---

## 🛠 Usage Guide
### Consumer Assistant Tab
Try asking the assistant:

>"I'm looking for something to help with digestive issues.">

>"What is the best yogurt to eat after a gym session?">

### Insights Dashboard Tab<br>
<img width="1816" height="549" alt="Assistant Screenshot" src="https://github.com/user-attachments/assets/be03ae9f-fd0d-43c4-8d9f-fe9899794454" /><br>
Review aggregated metrics including:

- Top consumer needs and personas.

- Distribution of intent and usage occasions.

New flavor requests and innovation signals.
---
## 🛡 Data Governance & Compliance<br>
<img width="1837" height="723" alt="Dashboard Screenshot" src="https://github.com/user-attachments/assets/0d8e18f2-426a-47db-b88b-231f7305c09b" /><br>
Guardrails: No medical claims; uses compliant language (e.g., "may support", "can help").
Privacy: No personally identifiable information (PII) is intentionally collected.

Anonymization: Conversations are stored in an anonymized, structured format.
---
## 📈 Future Roadmap
Channel Integration: Connection with the LINE Messaging API.

Enterprise Scaling: Deployment on Databricks for robust data governance.

Advanced Analytics: Integration with Power BI for real-time executive reporting.

Authentication: Session tracking and user-specific rate limiting.

---
## 🤝 Contact & License
Author: Patrick

Department: Danone Japan – Digital & Strategy

License: Internal / Demo Use Only

Disclaimer: This is a prototype for demonstration purposes. It is not intended to provide medical advice. Product claims should be validated by regulatory teams before production use.
