📊 AI Data Analytics & Chatbot

An interactive AI-powered data analytics and chatbot application built with Python, Streamlit, Pandas, Plotly, and Groq Cloud.

The application allows users to upload CSV or Excel datasets, clean and analyze the data, generate interactive visualizations, and ask natural-language questions about their datasets using a Groq-hosted Large Language Model (LLM).

🚀 Overview

AI Data Analytics & Chatbot combines traditional exploratory data analysis with Generative AI.

Instead of manually writing Python or Pandas code to understand a dataset, users can:

Upload a CSV or Excel dataset.
Automatically clean the data.
View dataset statistics.
Explore categorical and numerical information.
Generate interactive charts.
Ask questions about the dataset using natural language.
Receive AI-generated answers using the Groq API.
Store and restore datasets using a local SQLite database.
Application Workflow
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

✨ Features
📁 1. Dataset Upload

The application supports multiple tabular data formats:

CSV (.csv)
Excel (.xlsx)
Excel (.xls)

Uploaded files are processed using Pandas.

🧹 2. Automated Data Cleaning

The application provides an automated data-cleaning option.

The cleaning process can:

Remove duplicate rows.
Handle missing values.
Prepare the dataset for analysis.
Maintain the original dataset separately from the cleaned dataset.

The cleaned DataFrame is used for subsequent statistics, visualization, and chatbot analysis.

📋 3. Dataset Overview

The application provides a detailed overview of the uploaded dataset.

It displays:

Number of rows.
Number of columns.
Missing cells.
Memory usage.
First 10 rows.
Numerical statistics.
Categorical value frequencies.

Example:

Dataset Information

Rows              : 1000
Columns           : 12
Missing Cells     : 25
Memory Usage      : 125 KB

📊 4. Statistical Analysis

The application calculates descriptive statistics for numerical columns.

Examples include:

Count
Mean
Standard deviation
Minimum
Maximum
Quartiles

For categorical columns, the application calculates frequency distributions.

Example:

Category

Electronics    350
Clothing       280
Furniture      220
Other          150

📈 5. Interactive Visualizations

The application provides interactive Plotly visualizations.

Available chart types include:

Bar Chart

Used for comparing categories and numerical values.

Category → Value

Line Chart

Used for analyzing trends.

Time → Value

Scatter Plot

Used for analyzing relationships between two numerical variables.

Variable X ↔ Variable Y

Histogram

Used to understand the distribution of numerical data.

The number of bins can be adjusted.

Box Plot

Used to visualize:

Distribution
Median
Quartiles
Potential outliers
Correlation Heatmap

Used to visualize correlations between numerical columns.

🤖 6. AI Data Chatbot

The application includes an AI chatbot that allows users to ask natural-language questions about their uploaded dataset.

Example questions:

What is the average Sales?

What is the maximum Profit?

Which category occurs most frequently?

How many records are in the dataset?

What are the numerical statistics?

What is the relationship between Sales and Profit?

Which region has the highest number of records?


The chatbot uses dataset information and calculated statistics to generate an AI response.

⚡ Groq Cloud Integration

The AI chatbot uses Groq Cloud for LLM inference.

The project uses the OpenAI-compatible Python client:

from openai import OpenAI


but the client is configured to communicate with Groq:

base_url="https://api.groq.com/openai/v1"


Therefore:

The AI backend is Groq Cloud, not OpenAI and not Ollama.

The model configured in the chatbot is:

openai/gpt-oss-120b

🧠 AI Chatbot Architecture

The chatbot processing flow is:

User Question
      │
      ▼
Streamlit Chat Interface
      │
      ▼
ChatbotOrchestrator
      │
      ▼
Active DataFrame
      │
      ▼
Dataset Profiling
      │
      ├── Dataset Name
      ├── Number of Rows
      ├── Number of Columns
      ├── Column Names
      ├── Numerical Statistics
      └── Categorical Value Counts
      │
      ▼
Prompt Construction
      │
      ▼
Groq Cloud API
      │
      ▼
openai
