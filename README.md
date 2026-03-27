# Danone AI Consumer Assistant (RAG + Insights)

## Overview

This project is a prototype of an **AI-powered consumer assistant** designed for Danone Japan.

It demonstrates how conversational AI can:
- Answer consumer questions about health and products
- Recommend relevant Danone products
- Collect structured consumer insights from conversations
- Enable data-driven marketing and innovation

The solution combines:
- Retrieval-Augmented Generation (RAG)
- Controlled prompt design (compliance + tone)
- Conversation logging and insight extraction
- A lightweight analytics dashboard

---

## Key Features

### 1. AI Consumer Assistant
- Natural language interaction
- Product recommendation (e.g. Danone Bio, Oikos)
- Health-oriented explanations (compliant and non-medical)
<img width="1816" height="549" alt="image" src="https://github.com/user-attachments/assets/be03ae9f-fd0d-43c4-8d9f-fe9899794454" />

### 2. RAG (Retrieval-Augmented Generation)
- Uses curated product knowledge from local files
- Prevents hallucination
- Ensures brand-safe responses

### 3. Insight Extraction Layer
Each user interaction is converted into structured signals:
- Consumer need (e.g. digestion, protein)
- Intent (question, purchase intent, curiosity)
- Sentiment
- Persona
- Usage occasion
- Flavor requests
- Innovation signals
- New product requests

### 4. Consumer Insights Dashboard
- Visualizes trends from interactions
- Identifies emerging needs and opportunities
- Supports marketing and product innovation
<img width="1837" height="723" alt="image" src="https://github.com/user-attachments/assets/0d8e18f2-426a-47db-b88b-231f7305c09b" />

---

## Architecture
User → Streamlit UI → RAG (Chroma)
↓
OpenAI API
↓
Response + Insight Extraction
↓
CSV Log Storage
↓
Streamlit Dashboard

---

## Project Structure
├── app.py
├── data/
│ ├── bio.txt
│ ├── oikos.txt
│ └── ...
├── chroma_db/
├── consumer_insights_log.csv
├── requirements.txt
├── README.md
└── .env
---
## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <repo-name>
###2. Install dependencies
pip install -r requirements.txt
###3. Create a .env file

Create a file named .env in the project root and add:

OPENAI_API_KEY=your_api_key_here
###4. Add product knowledge files

Add .txt files in the data/ folder.

Examples:

bio.txt
oikos.txt

These files are used by the RAG layer to retrieve product information.

###5. Run the app
streamlit run app.py
####Usage
#####Consumer Assistant tab

Ask questions such as:

I have digestive issues
What should I eat after working out?

The assistant will:

retrieve relevant product data
generate a contextual answer
recommend suitable products when relevant
#####Insights Dashboard tab

The dashboard displays:

top consumer needs
intent distribution
recommended products
personas
usage occasions
flavor requests
innovation signals
new product requests
####Data Governance and Compliance

This prototype includes the following guardrails:

no medical claims
uses only curated product data through RAG
uses soft, compliant language such as may support and can help
no personally identifiable information is intentionally collected
conversations are stored in an anonymized, structured format for insight generation
####Cost Considerations

Typical MVP cost drivers:

LLM API cost: low for a small prototype
embeddings: negligible
infrastructure: minimal for local or Streamlit deployment
future production scaling cost: messaging volume and backend infrastructure
####Future Improvements

Possible next steps include:

integration with the LINE Messaging API
deployment on Databricks for enterprise data governance
vector search using enterprise infrastructure
real-time dashboards in Power BI
authentication and session tracking
rate limiting and cost monitoring
advanced persona clustering and topic analysis
####Business Value

This solution demonstrates how to:

move from campaign-based marketing to continuous interaction
generate first-party consumer insight
improve product recommendation relevance
support innovation through real consumer signals
####Disclaimer

This is a prototype for demonstration purposes only.

It is not intended to provide medical advice.
Product claims should be validated before production use.
Data governance policies should be applied before any official deployment.
####Author

Patrick
Danone Japan – Digital & Strategy

####License

Internal / Demo Use
