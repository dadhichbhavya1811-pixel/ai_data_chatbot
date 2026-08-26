# 📊 AI Data Analytics & Chatbot

An interactive **AI-powered data analytics and chatbot application** built with **Python, Streamlit, Pandas, Plotly, and Groq Cloud**.

The application allows users to upload CSV or Excel datasets, clean and analyze the data, generate interactive visualizations, and ask natural-language questions about their datasets using a Groq-hosted Large Language Model (LLM).

---

## 🚀 Overview

**AI Data Analytics & Chatbot** combines traditional exploratory data analysis with Generative AI.

Instead of manually writing Python or Pandas code to understand a dataset, users can:

- 📁 Upload CSV or Excel datasets
- 🧹 Automatically clean the data
- 📋 View dataset statistics
- 📊 Explore numerical and categorical information
- 📈 Generate interactive visualizations
- 🤖 Ask natural-language questions about the dataset
- ⚡ Receive AI-generated answers using the Groq API
- 🗄️ Store and restore datasets using a local SQLite database

---

## 🔄 Application Workflow

```text
                 ┌─────────────────────┐
                 │    Upload Dataset   │
                 │   CSV / Excel File  │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Data Processing   │
                 │  Cleaning & Checks  │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │  Dataset Analysis   │
                 │ Statistics & EDA    │
                 └──────────┬──────────┘
                            │
                 ┌──────────┴──────────┐
                 │                     │
                 ▼                     ▼
        ┌─────────────────┐   ┌──────────────────┐
        │  Visualization  │   │   AI Chatbot     │
        │  Plotly Charts  │   │   Groq Cloud     │
        └─────────────────┘   └────────┬─────────┘
                                       │
                                       ▼
                              ┌─────────────────┐
                              │ AI Data Insights│
                              └─────────────────┘
