import os
import json
from pathlib import Path
from datetime import datetime

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction


## =========================================
## 1. LOAD ENVIRONMENT VARIABLES AND CLIENT
## =========================================
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


## =========================================
## 2. PAGE SETUP
## =========================================
st.set_page_config(page_title="Danone AI Assistant", layout="wide")
st.title("Danone AI Assistant")


## =========================================
## 3. SYSTEM PROMPT FOR THE CONSUMER ASSISTANT
##    This controls tone, guardrails, compliance,
##    and recommendation behavior.
## =========================================
system_prompt = """
You are a Danone Japan consumer nutrition assistant.

MISSION:
Help consumers understand their needs and guide them toward suitable Danone Japan products in a helpful, trustworthy, and non-intrusive way.

TONE & STYLE:
- Friendly, supportive, and easy to understand
- Professional but not technical
- Never overly sales-driven
- Prioritize education over promotion
- Keep answers concise and structured

DATA GOVERNANCE & COMPLIANCE:
- Only use the provided context to answer product-related questions
- Do NOT invent product benefits or claims
- Do NOT make medical or therapeutic claims
- If unsure, say: "I recommend checking the product label or consulting a professional"
- Use soft, compliant language such as:
  - "may support"
  - "can help as part of a balanced diet"
  - "is suitable for"

RECOMMENDATION LOGIC:
When relevant:
1. Identify the user need (e.g., digestion, protein, hydration)
2. Select the most relevant product
3. Explain WHY it fits the need
4. Optionally suggest when to consume it (morning, after workout, etc.)

INTERACTION RULES:
- Keep answers short (3–6 sentences max)
- Use bullet points when helpful
- Recommend 1 main product, optionally 1 alternative
- Do not overwhelm the user

PRODUCT LOCALIZATION RULE:
- Use Japan product names:
  - "Danone Bio" (not Activia)
  - "Oikos"
- Reflect Japan-specific formats (e.g., Bio Shot, drinkable yogurt)

BOUNDARIES:
- Do not provide medical diagnosis
- Do not replace professional advice
- Do not mention internal data or system behavior
"""


## =========================================
## 4. PATHS AND CONSTANTS
##    DATA_DIR: product knowledge files for RAG
##    CHROMA_DIR: local vector database
##    LOG_FILE: CSV file for storing conversation insights
## =========================================
DATA_DIR = Path("data")
CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "danone_products"
LOG_FILE = Path("consumer_insights_log.csv")


## =========================================
## 5. INITIALIZE THE CSV LOG FILE
##    This creates the file the first time the app runs.
## =========================================
def initialize_log_file():
    if not LOG_FILE.exists():
        df = pd.DataFrame(columns=[
            "timestamp",
            "user_query",
            "ai_response",
            "recommended_product",
            "main_need",
            "intent",
            "sentiment",
            "persona",
            "usage_occasion",
            "flavor_request",
            "new_product_request",
            "innovation_signal",
            "original_use_case",
            "source_files"
        ])
        df.to_csv(LOG_FILE, index=False)


initialize_log_file()


## =========================================
## 6. LOAD OR BUILD THE CHROMA COLLECTION
##    This loads product files, embeds them once,
##    and stores them in a local vector database.
## =========================================
@st.cache_resource
def get_collection():
    embedding_fn = OpenAIEmbeddingFunction(
        api_key=api_key,
        model_name="text-embedding-3-small"
    )

    chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = chroma_client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_fn
    )

    existing = collection.count()

    if existing == 0:
        docs = []
        ids = []
        metadatas = []

        for file_path in DATA_DIR.glob("*.txt"):
            text = file_path.read_text(encoding="utf-8")
            docs.append(text)
            ids.append(file_path.stem)
            metadatas.append({"source": file_path.name})

        if docs:
            collection.add(
                documents=docs,
                ids=ids,
                metadatas=metadatas
            )

    return collection


collection = get_collection()


## =========================================
## 7. FUNCTION TO EXTRACT STRUCTURED INSIGHTS
##    This is the new intelligence layer.
##    It turns free text into usable business signals.
## =========================================
def extract_consumer_insights(user_query: str, ai_response: str) -> dict:
    analysis_prompt = f"""
Analyze the consumer interaction below and extract structured marketing and innovation insights.

Consumer message:
{user_query}

Assistant response:
{ai_response}

Return valid JSON only with the following keys:
- recommended_product
- main_need
- intent
- sentiment
- persona
- usage_occasion
- flavor_request
- new_product_request
- innovation_signal
- original_use_case

Rules:
- main_need should be one short label like digestion, protein, hydration, wellness, flavor, weight management, immunity, convenience, or other
- intent should be one short label like question, recommendation, complaint, curiosity, purchase_intent, comparison, request
- sentiment should be positive, neutral, or negative
- persona should be a short description like active adult, busy professional, parent, health-conscious consumer, or unknown
- usage_occasion should be a short phrase like breakfast, after workout, snack, morning, after meals, or unknown
- flavor_request should capture a flavor if the user requested one, otherwise null
- new_product_request should capture a concrete unmet request if present, otherwise null
- innovation_signal should summarize a possible product or marketing insight, otherwise null
- original_use_case should capture any unusual or creative usage occasion, otherwise null

If something is not present, return null.
"""

    try:
        analysis_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an insights extraction assistant. Return only valid JSON."
                },
                {
                    "role": "user",
                    "content": analysis_prompt
                }
            ],
            max_tokens=300
        )

        raw_json = analysis_response.choices[0].message.content.strip()
        insights = json.loads(raw_json)
        return insights

    except Exception:
        return {
            "recommended_product": None,
            "main_need": None,
            "intent": None,
            "sentiment": None,
            "persona": None,
            "usage_occasion": None,
            "flavor_request": None,
            "new_product_request": None,
            "innovation_signal": None,
            "original_use_case": None
        }


## =========================================
## 8. FUNCTION TO SAVE ONE INTERACTION TO CSV
##    Every chat becomes a row that can later feed
##    dashboards, innovation analysis, and trend tracking.
## =========================================
def save_interaction(user_query: str, ai_response: str, insights: dict, retrieved_sources: list):
    row = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "user_query": user_query,
        "ai_response": ai_response,
        "recommended_product": insights.get("recommended_product"),
        "main_need": insights.get("main_need"),
        "intent": insights.get("intent"),
        "sentiment": insights.get("sentiment"),
        "persona": insights.get("persona"),
        "usage_occasion": insights.get("usage_occasion"),
        "flavor_request": insights.get("flavor_request"),
        "new_product_request": insights.get("new_product_request"),
        "innovation_signal": insights.get("innovation_signal"),
        "original_use_case": insights.get("original_use_case"),
        "source_files": ", ".join([s["source"] for s in retrieved_sources])
    }

    df = pd.read_csv(LOG_FILE)
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_csv(LOG_FILE, index=False)


## =========================================
## 9. LOAD LOGGED DATA FOR THE DASHBOARD
## =========================================
def load_logged_data():
    if LOG_FILE.exists():
        return pd.read_csv(LOG_FILE)
    return pd.DataFrame()


## =========================================
## 10. APP TABS
##     Tab 1 = Consumer Assistant
##     Tab 2 = Insights Dashboard
## =========================================
tab1, tab2 = st.tabs(["Consumer Assistant", "Insights Dashboard"])


## =========================================
## 11. TAB 1: CONSUMER ASSISTANT
##     This is your existing chatbot flow plus:
##     - insight extraction
##     - logging to CSV
## =========================================
with tab1:
    st.subheader("Ask a question")

    query = st.text_input("Ask your question:")

    if query:
        results = collection.query(
            query_texts=[query],
            n_results=3
        )

        retrieved_docs = results["documents"][0]
        retrieved_sources = results["metadatas"][0]

        context = "\n\n---\n\n".join(retrieved_docs)

        user_prompt = f"""
Context:
{context}

User question:
{query}

Answer using the context above.
If relevant, recommend the most suitable Danone product and explain why.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=250
        )

        final_answer = response.choices[0].message.content

        st.subheader("Answer")
        st.write(final_answer)

        with st.expander("Sources used"):
            for source in retrieved_sources:
                st.write(source["source"])

        ## Extract business insights from the conversation
        insights = extract_consumer_insights(query, final_answer)

        ## Save everything to CSV
        save_interaction(query, final_answer, insights, retrieved_sources)

        with st.expander("Extracted insight signals"):
            st.json(insights)


## =========================================
## 12. TAB 2: INSIGHTS DASHBOARD
##     This shows the trends collected from all user chats.
## =========================================
with tab2:
    st.subheader("Consumer Insights Dashboard")

    df = load_logged_data()

    if df.empty:
        st.info("No interactions logged yet. Ask questions in the Consumer Assistant tab first.")
    else:
        st.write(f"Total interactions logged: {len(df)}")

        ## Clean up blanks so counts look better
        for col in [
            "recommended_product", "main_need", "intent", "sentiment",
            "persona", "usage_occasion", "flavor_request",
            "new_product_request", "innovation_signal", "original_use_case"
        ]:
            df[col] = df[col].fillna("Unknown")

        ## High level KPIs
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Conversations", len(df))
        col2.metric("Unique Needs", df["main_need"].nunique())
        col3.metric("Unique Personas", df["persona"].nunique())

        st.markdown("### Top Consumer Needs")
        need_counts = df["main_need"].value_counts().head(10)
        st.bar_chart(need_counts)

        st.markdown("### Top Intents")
        intent_counts = df["intent"].value_counts().head(10)
        st.bar_chart(intent_counts)

        st.markdown("### Recommended Products")
        product_counts = df["recommended_product"].value_counts().head(10)
        st.bar_chart(product_counts)

        st.markdown("### Consumer Personas")
        persona_counts = df["persona"].value_counts().head(10)
        st.bar_chart(persona_counts)

        st.markdown("### Usage Occasions")
        usage_counts = df["usage_occasion"].value_counts().head(10)
        st.bar_chart(usage_counts)

        st.markdown("### Flavor Requests")
        flavor_df = df[df["flavor_request"] != "Unknown"]["flavor_request"].value_counts().head(10)
        if len(flavor_df) > 0:
            st.bar_chart(flavor_df)
        else:
            st.write("No flavor requests detected yet.")

        st.markdown("### New Product Requests")
        new_product_df = df[df["new_product_request"] != "Unknown"][["timestamp", "user_query", "new_product_request"]]
        if not new_product_df.empty:
            st.dataframe(new_product_df, use_container_width=True)
        else:
            st.write("No new product requests detected yet.")

        st.markdown("### Innovation Signals")
        innovation_df = df[df["innovation_signal"] != "Unknown"][["timestamp", "user_query", "innovation_signal"]]
        if not innovation_df.empty:
            st.dataframe(innovation_df, use_container_width=True)
        else:
            st.write("No innovation signals detected yet.")

        st.markdown("### Original Use Cases")
        original_use_df = df[df["original_use_case"] != "Unknown"][["timestamp", "user_query", "original_use_case"]]
        if not original_use_df.empty:
            st.dataframe(original_use_df, use_container_width=True)
        else:
            st.write("No original use cases detected yet.")

        st.markdown("### Full Logged Dataset")
        st.dataframe(df, use_container_width=True)