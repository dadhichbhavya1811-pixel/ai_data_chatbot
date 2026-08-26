# 📊 AI-Powered Data Analytics Chatbot

An interactive **AI-powered data analytics and visualization application** built with **Python, Streamlit, Pandas, Plotly, SQLite, and Groq LLMs**.

The application allows users to upload CSV or Excel datasets, automatically clean and analyze the data, generate interactive visualizations, explore statistical insights, and ask questions about their dataset using natural language through an AI chatbot.

---

## 🚀 Project Overview

**AI Data Analytics Chatbot** is an end-to-end data analysis application designed to simplify the process of exploring structured datasets.

Instead of manually writing Python or SQL queries for every analysis, users can upload a dataset and interact with it through a visual dashboard and an AI-powered conversational interface.

### The application provides:

* 📁 CSV and Excel file upload
* 🧹 Automated data cleaning
* 📊 Dataset statistics and metadata
* 🔍 Exploratory Data Analysis (EDA)
* 📈 Interactive Plotly visualizations
* 🤖 Natural-language AI data analysis
* 🗄️ Local SQLite dataset caching
* 💬 Conversational chat interface
* 📋 Data preview and descriptive statistics
* ⚠️ Outlier detection using the IQR method
* 📝 Application logging
* 💾 Dataset restoration from local cache

---

## ✨ Key Features

### 📁 1. Data Ingestion

Upload datasets directly through the Streamlit interface.

Supported formats:

* `.csv`
* `.xlsx`
* `.xls`

The application loads uploaded datasets into Pandas DataFrames for further processing.

---

### 🧹 2. Automated Data Cleaning

The project includes a dedicated `DataCleaner` module for preparing datasets before analysis.

The cleaning pipeline can:

* Remove duplicate rows
* Detect missing values
* Fill missing numerical values using the median
* Fill missing categorical/text values using `"Unknown"`
* Preserve the original uploaded dataset through DataFrame copying

This helps create a cleaner dataset before statistical analysis and AI-based querying.

---

### 📊 3. Dataset Overview & Statistics

After uploading a dataset, the application provides an overview containing:

* Total number of records
* Total number of columns/features
* Missing cell count
* Memory usage
* First 10 rows of the dataset
* Numerical descriptive statistics
* Categorical information

The statistics functionality is implemented through the `StatisticsEngine` module.

---

### 🔍 4. Exploratory Data Analysis

The EDA engine provides analytical functionality for understanding the structure and patterns of the dataset.

Current analytical capabilities include:

* Numerical analysis
* Correlation analysis
* Outlier detection
* IQR-based statistical analysis
* Dataset profiling

The outlier detection system uses the **Interquartile Range (IQR)** method:

```text
IQR = Q3 - Q1

Lower Bound = Q1 - 1.5 × IQR

Upper Bound = Q3 + 1.5 × IQR
```

Values outside these boundaries are identified as potential outliers.

---

### 📈 5. Interactive Data Visualization

The project uses **Plotly** to create interactive charts.

Supported visualization functionality includes:

* 📊 Bar charts
* 📈 Line charts
* 🔵 Scatter plots
* 📉 Histograms
* 📦 Box plots
* 🔥 Correlation visualizations

Charts are generated dynamically based on the selected dataset columns.

---

### 🤖 6. AI Data Chatbot

The main feature of the project is the AI-powered data chatbot.

Users can ask questions about their uploaded dataset using natural language.

For example:

```text
What is the average sales?

Which product generated the highest revenue?

Show me the top 10 customers.

Which category has the most orders?

What is the relationship between sales and profit?

Are there any unusual values in the dataset?

Summarize the important insights from this dataset.
```

The chatbot orchestrator connects the active Pandas DataFrame, statistics engine, database layer, prompts, and LLM API.

The current implementation uses an **OpenAI-compatible client configured for Groq Cloud** and the model:

```text
openai/gpt-oss-120b
```

---

## 🧠 AI Architecture

The chatbot follows a modular architecture:

```text
User Question
      │
      ▼
Streamlit Chat Interface
      │
      ▼
ChatbotOrchestrator
      │
      ├── Active Pandas DataFrame
      │
      ├── Statistics Engine
      │
      ├── Database Manager
      │
      ├── Prompt Templates
      │
      └── Groq LLM
              │
              ▼
        AI Generated Response
```

This architecture separates the user interface, data processing, database storage, analytics, and AI reasoning components.

---

## 🗄️ 7. Local SQLite Cache

The project includes a local SQLite database for dataset caching.

The database manager:

* Creates the local database directory when required
* Saves DataFrames as SQL tables
* Loads previously cached datasets
* Lists available cached tables
* Allows restoration of previously processed datasets

The default database location is:

```text
data/chatbot_storage.db
```

This allows users to restore previously processed datasets without uploading them again.

---

## 🖥️ Application Interface

The Streamlit application is divided into three primary sections:

### 📋 Overview & Statistics

Provides:

* Dataset metadata
* Row and column counts
* Missing values
* Memory usage
* Data preview
* Descriptive statistics

### 📈 Interactive Visualizations

Provides interactive data charts for visual exploration.

### 🤖 AI Data Chatbot

Provides a conversational interface where users can ask natural-language questions about their dataset.

---

## 🛠️ Technology Stack

| Technology           | Purpose                                |
| -------------------- | -------------------------------------- |
| Python               | Core programming language              |
| Streamlit            | Web application and UI                 |
| Pandas               | Data processing and analysis           |
| NumPy                | Numerical computation                  |
| Plotly               | Interactive visualization              |
| Matplotlib           | Data visualization support             |
| Seaborn              | Statistical visualization support      |
| Scikit-learn         | Machine learning/data analysis support |
| SQLite               | Local dataset caching                  |
| SQL                  | Structured local data storage          |
| LangChain            | LLM application framework support      |
| Ollama               | Local LLM integration support          |
| Groq API             | Cloud LLM inference                    |
| OpenAI Python Client | OpenAI-compatible API interface        |
| python-dotenv        | Environment configuration              |
| FPDF2                | PDF generation support                 |

---

## 📂 Project Structure

```text
ai_data_chatbot/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   │
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── chatbot.py
│   │   ├── data_cleaner.py
│   │   ├── data_loader.py
│   │   ├── database.py
│   │   ├── eda.py
│   │   ├── export.py
│   │   ├── llm.py
│   │   ├── prompts.py
│   │   ├── statistics.py
│   │   └── visualizer.py
│   │
│   └── utils/
│       ├── __init__.py
│       └── logger.py
│
└── data/
    └── chatbot_storage.db
```

---

## 🔎 Module Description

### `app.py`

Main Streamlit application.

Responsible for:

* Streamlit page configuration
* File uploading
* Session-state management
* Dataset loading
* Data cleaning
* Cache restoration
* Statistics dashboard
* Visualization interface
* AI chatbot interface

---

### `data_loader.py`

Handles CSV and Excel dataset loading.

It supports:

* File paths
* Streamlit `UploadedFile` objects
* CSV files
* Excel files

---

### `data_cleaner.py`

Responsible for automated dataset cleaning.

Main operations include:

```python
remove_duplicates()
clean_missing_values()
```

---

### `database.py`

Provides local SQLite storage functionality.

It handles:

```text
DataFrame
   ↓
SQLite Table
   ↓
Local Cache
   ↓
Dataset Restoration
```

---

### `statistics.py`

Provides statistical analysis and dataset metadata.

Used to generate:

* Dataset dimensions
* Missing-value information
* Numerical statistics
* Categorical summaries
* Analytical metrics

---

### `eda.py`

Provides exploratory data analysis functionality.

It includes analytical operations such as:

* Correlation analysis
* Outlier detection
* IQR calculations
* Numerical data profiling

---

### `visualizer.py`

Creates interactive Plotly charts.

Example methods include:

```python
plot_bar()
plot_line()
plot_scatter()
plot_histogram()
```

---

### `chatbot.py`

Acts as the central AI orchestration layer.

It connects:

```text
Dataset
   +
Statistics
   +
Database
   +
Prompt Templates
   +
Groq LLM
```

and produces AI-generated responses based on the active dataset.

---

### `prompts.py`

Contains prompt templates used by the chatbot to structure AI interactions and data-analysis requests.

---

### `llm.py`

Contains LLM-related functionality and integration support.

---

### `export.py`

Provides functionality related to exporting analytical/data results.

---

### `config.py`

Centralizes application configuration.

The configuration supports environment variables such as:

```text
APP_NAME
LOG_LEVEL
OLLAMA_MODEL
OLLAMA_BASE_URL
```

---

### `logger.py`

Provides centralized application logging for different modules.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/dadhichbhavya1811-pixel/ai_data_chatbot.git
```

### 2. Navigate to the project directory

```bash
cd ai_data_chatbot
```

### 3. Create a virtual environment

Windows:

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows Command Prompt:

```bash
venv\Scripts\activate
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

---

## 📦 Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

The current repository pins the major dependencies, including Streamlit 1.35.0, Pandas 2.2.2, NumPy 1.26.4, Plotly 5.22.0, Scikit-learn 1.5.0, LangChain 0.2.1, Ollama 0.2.1, and python-dotenv 1.0.1.

---

## 🔐 Environment Configuration

The chatbot requires a Groq API key.

Create a `.env` file in the project root:

```text
GROQ_API_KEY=your_groq_api_key_here
```

The application reads the API key from either Streamlit secrets or the environment.

### Optional configuration

```text
APP_NAME=AI Data Chatbot
LOG_LEVEL=INFO
OLLAMA_MODEL=llama3
OLLAMA_BASE_URL=http://localhost:11434
```

> ⚠️ Never commit your API key to GitHub.

Make sure `.env` is included in `.gitignore`.

---

## ▶️ Run the Application

Start the Streamlit application using:

```bash
streamlit run app.py
```

After starting the application, Streamlit will provide a local URL similar to:

```text
http://localhost:8501
```

Open the URL in your browser.

---

## 🧪 How to Use

### Step 1 — Start the application

```bash
streamlit run app.py
```

### Step 2 — Upload your dataset

Use the sidebar to upload:

```text
CSV
XLSX
XLS
```

### Step 3 — Clean the dataset

Enable:

```text
Apply Automated Data Cleaning
```

The application removes duplicates and handles missing values.

### Step 4 — Explore the data

Open:

```text
Overview & Statistics
```

to inspect the dataset.

### Step 5 — Create visualizations

Open:

```text
Interactive Visualizations
```

and explore the available charts.

### Step 6 — Ask the AI chatbot

Open:

```text
AI Data Chatbot
```

and ask questions about your data.

---

## 💡 Example Questions

You can ask questions such as:

```text
Give me an overview of this dataset.
```

```text
How many rows and columns are there?
```

```text
Which column contains the most missing values?
```

```text
What is the average value of the sales column?
```

```text
Which category has the highest revenue?
```

```text
Find the top 10 products by sales.
```

```text
What are the major trends in this dataset?
```

```text
Are there any outliers?
```

```text
Give me the most important business insights.
```

---

## 🔄 Data Processing Pipeline

The complete application workflow can be represented as:

```text
                ┌───────────────────┐
                │   Upload Dataset  │
                │    CSV / Excel    │
                └─────────┬─────────┘
                          │
                          ▼
                ┌───────────────────┐
                │   Data Loader     │
                │     Pandas        │
                └─────────┬─────────┘
                          │
                          ▼
                ┌───────────────────┐
                │  Data Cleaning    │
                │ • Duplicates      │
                │ • Missing Values  │
                └─────────┬─────────┘
                          │
                          ▼
              ┌─────────────────────────┐
              │   Processed DataFrame   │
              └────────────┬────────────┘
                           │
             ┌─────────────┼──────────────┐
             │             │              │
             ▼             ▼              ▼
      ┌────────────┐ ┌────────────┐ ┌──────────────┐
      │ Statistics │ │    EDA     │ │ Visualization│
      └──────┬─────┘ └──────┬─────┘ └───────┬──────┘
             │              │               │
             └──────────────┼───────────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │  AI Chatbot     │
                   │   Groq LLM      │
                   └────────┬────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │ AI Data Insights│
                   └─────────────────┘
```

---

## 🏗️ Architecture

The project follows a modular architecture:

```text
                  Streamlit UI
                       │
                       ▼
              Application Controller
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
   Data Layer     Analytics Layer   AI Layer
        │              │              │
        ▼              ▼              ▼
 Data Loader       Statistics      Chatbot
 Data Cleaner      EDA             LLM
 Database          Visualizer       Prompts
        │              │              │
        └──────────────┼──────────────┘
                       │
                       ▼
                  Final Results
```

---

## 📌 Current Repository Components

The repository currently contains:

```text
app.py
requirements.txt
src/
├── config.py
├── modules/
│   ├── chatbot.py
│   ├── data_cleaner.py
│   ├── data_loader.py
│   ├── database.py
│   ├── eda.py
│   ├── export.py
│   ├── llm.py
│   ├── prompts.py
│   ├── statistics.py
│   └── visualizer.py
└── utils/
    └── logger.py
```

These modules separate data ingestion, cleaning, analysis, visualization, storage, AI processing, configuration, and logging responsibilities.

---

## 🔒 Security

For security:

1. Do not hard-code API keys.
2. Store secrets in `.env` or Streamlit secrets.
3. Add `.env` to `.gitignore`.
4. Never upload private datasets to a public repository.
5. Rotate API keys if they are accidentally exposed.

Example `.gitignore`:

```text
.env
.venv/
venv/
__pycache__/
*.pyc
data/*.db
.streamlit/secrets.toml
```

---

## ⚠️ Important Notes

### LLM API

The current chatbot implementation initializes an OpenAI-compatible client with the Groq endpoint:

```text
https://api.groq.com/openai/v1
```

and uses:

```text
openai/gpt-oss-120b
```

as its configured production model.

Therefore, a valid `GROQ_API_KEY` is required for the AI chatbot functionality.

### Local Database

The SQLite cache is created locally and is not intended to be committed to the GitHub repository.

### Dataset Size

Very large datasets may require additional memory and processing time because the application loads datasets into Pandas DataFrames.

---

## 🐛 Troubleshooting

### Streamlit command not found

Try:

```bash
python -m streamlit run app.py
```

### Virtual environment not activated

Windows CMD:

```bash
venv\Scripts\activate
```

Then verify:

```bash
python --version
```

### Dependency installation problem

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Then:

```bash
pip install -r requirements.txt
```

### Groq API error

Verify that your API key exists:

```text
GROQ_API_KEY=your_actual_api_key
```

Restart Streamlit after changing environment variables.

### ModuleNotFoundError

Make sure you are running the command from the project root:

```text
ai_data_chatbot/
```

Then run:

```bash
streamlit run app.py
```

---

## 🚧 Future Improvements

Possible future enhancements include:

* [ ] Support for larger datasets
* [ ] SQL query generation through natural language
* [ ] More advanced AI-generated insights
* [ ] Automatic chart recommendations
* [ ] Dataset profiling reports
* [ ] PDF/Excel report generation
* [ ] User authentication
* [ ] Cloud database support
* [ ] Deployment to Streamlit Cloud
* [ ] Docker support
* [ ] Automated testing
* [ ] Machine learning prediction modules
* [ ] Time-series forecasting
* [ ] Advanced anomaly detection
* [ ] Multiple dataset comparison
* [ ] Conversational memory improvements

---

## 🎓 Academic / Internship Project

This project demonstrates practical implementation of:

* Python programming
* Object-oriented programming
* Data preprocessing
* Exploratory Data Analysis
* Statistical analysis
* Data visualization
* SQL/SQLite database management
* Generative AI
* Large Language Models
* Streamlit application development
* Modular software architecture
* API integration

It can be used as an academic project, internship project, or portfolio project for demonstrating **Data Analytics + AI + Python development** skills.

---

## 👨‍💻 Author

**Bhavya Dadhich**

M.Sc. IT | Data Analytics | Python | AI | Machine Learning

GitHub:
https://github.com/dadhichbhavya1811-pixel

---

## ⭐ If You Find This Project Useful

If this project helped you understand AI-powered data analytics, consider giving the repository a ⭐ star on GitHub.

---

## 📄 License

This project is intended for educational, academic, and portfolio purposes.

---

## 🔗 Repository

**AI Data Analytics Chatbot**

https://github.com/dadhichbhavya1811-pixel/ai_data_chatbot
