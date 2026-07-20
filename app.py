import sys
import os

# Ensure project root is in path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import pandas as pd

# Safe module imports
try:
    from src.modules.dataloader import DataLoader
except ImportError:
    from src.modules.data_loader import DataLoader

try:
    from src.modules.cleaner import DataCleaner
except ImportError:
    from src.modules.data_cleaner import DataCleaner

from src.modules.statistics import StatisticsEngine
from src.modules.eda import EDAEngine
from src.modules.visualizer import DataVisualizer
from src.modules.chatbot import ChatbotOrchestrator
from src.utils.logger import setup_logger

logger = setup_logger("streamlit_app")

# Page Configuration
st.set_page_config(
    page_title="AI Data Analytics Chatbot",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session States
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = ChatbotOrchestrator()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "raw_df" not in st.session_state:
    st.session_state.raw_df = None

if "cleaned_df" not in st.session_state:
    st.session_state.cleaned_df = None

# Title & Header
st.title("📊 AI-Powered Local Data Analytics & Chatbot Engine")
st.markdown("Upload tabular datasets, perform automated data cleaning, explore interactive charts, and query your data using a local LLM.")

# --- SIDEBAR: DATA INGESTION & CACHE MANAGEMENT ---
st.sidebar.header("📁 Data Source Management")

uploaded_file = st.sidebar.file_uploader(
    "Upload a CSV or Excel file", 
    type=["csv", "xlsx", "xls"]
)

if uploaded_file is not None:
    try:
        # File Loading Attempt
        df_loaded = None
        
        # 1. Direct Pandas read (Most reliable for Streamlit UploadedFile objects)
        if uploaded_file.name.endswith(".csv"):
            df_loaded = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith((".xlsx", ".xls")):
            df_loaded = pd.read_excel(uploaded_file)
        
        # 2. Fallback to DataLoader class if custom processing is required
        if df_loaded is None:
            try:
                loader = DataLoader(uploaded_file)
                df_loaded = loader.load_data()
            except Exception:
                loader = DataLoader()
                df_loaded = loader.load_data(uploaded_file)

        st.session_state.raw_df = df_loaded

        if st.session_state.raw_df is not None:
            st.sidebar.success(f"Loaded: {uploaded_file.name}")
            
           # Auto-Clean Option
            if st.sidebar.checkbox("Apply Automated Data Cleaning", value=True):
                cleaner = DataCleaner(st.session_state.raw_df)
                
                if hasattr(cleaner, 'clean_missing_values'):
                    # Execute duplicate removal first if method exists
                    if hasattr(cleaner, 'remove_duplicates'):
                        cleaner.remove_duplicates()
                    st.session_state.cleaned_df = cleaner.clean_missing_values()
                elif hasattr(cleaner, 'clean_data'):
                    st.session_state.cleaned_df = cleaner.clean_data()
                elif hasattr(cleaner, 'clean'):
                    st.session_state.cleaned_df = cleaner.clean()
                elif hasattr(cleaner, 'process'):
                    st.session_state.cleaned_df = cleaner.process()
                else:
                    st.sidebar.warning("Cleaner method not found, using raw data.")
                    st.session_state.cleaned_df = st.session_state.raw_df.copy()
            else:
                st.session_state.cleaned_df = st.session_state.raw_df.copy()
            
            # Sync Active Dataset with Chatbot Orchestrator
            table_name = uploaded_file.name.split(".")[0].replace(" ", "_").lower()
            st.session_state.orchestrator.set_active_dataset(
                table_name=table_name, 
                df=st.session_state.cleaned_df
            )
    except Exception as e:
        st.sidebar.error(f"Error loading file: {str(e)}")
        st.error(f"Failed to process uploaded file: {str(e)}")

# Cache / Historical Storage Selector
st.sidebar.markdown("---")
st.sidebar.subheader("🗄️ Local SQL Cache Repository")
all_tables = st.session_state.orchestrator.db_manager.get_all_tables()

if all_tables:
    selected_table = st.sidebar.selectbox("Load Cached Table", options=["None"] + all_tables)
    if selected_table != "None":
        if st.sidebar.button("Restore Selected Cache"):
            success = st.session_state.orchestrator.load_dataset_from_cache(selected_table)
            if success:
                st.session_state.cleaned_df = st.session_state.orchestrator.current_df
                st.session_state.raw_df = st.session_state.cleaned_df.copy()
                st.sidebar.success(f"Restored workspace state: '{selected_table}'")
                st.rerun()

# --- MAIN DASHBOARD BODY ---
if st.session_state.cleaned_df is not None:
    df = st.session_state.cleaned_df
    
    # Initialize Engines
    stats_engine = StatisticsEngine(df)
    eda_engine = EDAEngine(df)
    visualizer = DataVisualizer(df)
    
    # Layout Tabs
    tab1, tab2, tab3 = st.tabs(["📋 Overview & Statistics", "📈 Interactive Visualizations", "🤖 AI Data Chatbot"])
    
    # --- TAB 1: OVERVIEW & STATISTICS ---
    with tab1:
        st.header("Dataset Overview & Metadata")
        
        # Key Metrics Summary Cards
        metadata = stats_engine.get_dataset_metadata()
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Records (Rows)", metadata.get("total_records", 0))
        col2.metric("Total Features (Columns)", metadata.get("total_attributes", 0))
        col3.metric("Missing Cell Count", metadata.get("total_nulls", 0))
        col4.metric("Memory Usage", f"{df.memory_usage().sum() / 1024:.2f} KB")
        
        st.markdown("---")
        
        # Data Preview Table
        st.subheader("Data Preview (Top 10 Rows)")
        st.dataframe(df.head(10), use_container_width=True)
        
        # Summary Statistics Tables
        st.subheader("Descriptive Statistics Matrix")
        summaries = stats_engine.generate_summary_statistics()
        
        if "numeric" in summaries and summaries["numeric"] is not None and hasattr(summaries["numeric"], 'empty') and not summaries["numeric"].empty:
            st.markdown("**Numerical Feature Metrics**")
            st.dataframe(summaries["numeric"], use_container_width=True)
            
        if "categorical" in summaries and summaries["categorical"] is not None and len(summaries["categorical"]) > 0:
            st.markdown("**Categorical Feature Metrics**")
            if isinstance(summaries["categorical"], dict):
                for cat_col, freq_df in summaries["categorical"].items():
                    with st.expander(f"Frequency Distribution: {cat_col}"):
                        st.dataframe(freq_df, use_container_width=True)
            elif hasattr(summaries["categorical"], 'empty') and not summaries["categorical"].empty:
                st.dataframe(summaries["categorical"], use_container_width=True)

    # --- TAB 2: INTERACTIVE VISUALIZATIONS ---
    with tab2:
        st.header("Exploratory Data Graphics")
        
        chart_type = st.selectbox(
            "Select Chart Type", 
            ["Bar Chart", "Line Chart", "Scatter Plot", "Histogram", "Box Plot", "Correlation Heatmap"]
        )
        
        columns = list(df.columns)
        numeric_columns = list(df.select_dtypes(include=['number']).columns)
        
        if chart_type == "Bar Chart" and len(columns) >= 2:
            c1, c2 = st.columns(2)
            x_col = c1.selectbox("X-Axis (Category)", columns, index=0)
            y_col = c2.selectbox("Y-Axis (Value)", numeric_columns if numeric_columns else columns, index=0)
            fig = visualizer.plot_bar(x_col, y_col)
            st.plotly_chart(fig, use_container_width=True)
            
        elif chart_type == "Line Chart" and len(columns) >= 2:
            c1, c2 = st.columns(2)
            x_col = c1.selectbox("X-Axis (Time/Sequence)", columns, index=0)
            y_col = c2.selectbox("Y-Axis (Value)", numeric_columns if numeric_columns else columns, index=0)
            fig = visualizer.plot_line(x_col, y_col)
            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Scatter Plot" and len(numeric_columns) >= 2:
            c1, c2 = st.columns(2)
            x_col = c1.selectbox("X-Axis Variable", numeric_columns, index=0)
            y_col = c2.selectbox("Y-Axis Variable", numeric_columns, index=1 if len(numeric_columns) > 1 else 0)
            fig = visualizer.plot_scatter(x_col, y_col)
            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Histogram" and len(numeric_columns) >= 1:
            col = st.selectbox("Select Feature for Distribution Analysis", numeric_columns, index=0)
            bins = st.slider("Number of Bins", min_value=5, max_value=100, value=30)
            fig = visualizer.plot_histogram(col, bins=bins)
            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Box Plot" and len(numeric_columns) >= 1:
            col = st.selectbox("Select Target Variable for Outlier Detection", numeric_columns, index=0)
            fig = visualizer.plot_boxplot(y_col=col)
            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Correlation Heatmap":
            corr_df = eda_engine.calculate_correlation_matrix()
            if not corr_df.empty:
                fig = visualizer.plot_correlation_heatmap(corr_df)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Insufficient numerical features to compute linear correlation matrices.")

    # --- TAB 3: AI DATA CHATBOT ---
    with tab3:
        st.header("💬 Query Your Data (Local LLM)")
        st.markdown("Ask natural language questions about your dataset trends, minimums, maximums, distributions, or calculations.")
        
        # Display Historical Chat Thread
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat Input Interface
        if user_prompt := st.chat_input("e.g., What is the average value of Sales?"):
            # Render User Query
            st.session_state.chat_history.append({"role": "user", "content": user_prompt})
            with st.chat_message("user"):
                st.markdown(user_prompt)

            # Generate and Render AI Response
            with st.chat_message("assistant"):
                with st.spinner("Analyzing dataset with local AI model..."):
                    response = st.session_state.orchestrator.process_user_query(user_prompt)
                    st.markdown(response)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})

else:
    # Empty State Page
    st.info("👆 Please upload a CSV or Excel dataset file in the left sidebar to begin your analysis session.")