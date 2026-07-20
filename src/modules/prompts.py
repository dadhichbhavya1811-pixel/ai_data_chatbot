from typing import Dict, Any

class PromptTemplates:
    """
    Static repository class holding structured prompt engineering templates 
    for data analysis and insight generation workflows.
    """

    @staticmethod
    def get_analysis_prompt(metadata: Dict[str, Any], numeric_summary: str, user_query: str) -> str:
        """
        Constructs a highly structured data science prompt context block forcing 
        the LLM to answer user inquiries using rigorous mathematical reasoning.
        
        Args:
            metadata (Dict[str, Any]): Structural dataset parameters mapping attributes and row totals.
            numeric_summary (str): Transposed string layout representation of descriptive statistics.
            user_query (str): The natural language inquiry typed by the client.
            
        Returns:
            str: The interpolated complete instruction string prompt block.
        """
        return f"""
You are an expert Senior Data Scientist and Business Intelligence Analyst. Your task is to analyze the provided dataset profile metrics and answer the user's natural language question accurately based ONLY on the mathematical realities provided.

--- DATASET STRUCTURAL PROFILE ---
Total Rows/Records: {metadata.get('total_records')}
Total Columns/Attributes: {metadata.get('total_attributes')}
Column Schema & Data Types: {metadata.get('data_types')}

--- DESCRIPTIVE STATISTICAL MATRIX SUMMARY ---
{numeric_summary}

--- USER OBJECTIVE INQUIRY ---
User Question: {user_query}

--- INSTRUCTIONAL ANALYTICAL GUIDELINES ---
1. Base your inferences strictly on the provided dataset profile metrics and summary charts.
2. If you need to perform calculations, explicitly detail the mathematical steps or variables derived from the data.
3. Keep your analysis concise, professional, clear, and actionable. Avoid rambling or vague generalizations.
4. If the data provided does not contain enough evidence to confidently answer the question, clearly state the missing information required rather than guessing.

Expert Analytical Answer:
"""

    @staticmethod
    def get_auto_insights_prompt(metadata: Dict[str, Any], numeric_summary: str) -> str:
        """
        Constructs a prompt instructing the LLM to scan dataset distributions 
        and automatically generate structural observations and data narratives.
        
        Args:
            metadata (Dict[str, Any]): Structural dataset parameters mapping.
            numeric_summary (str): Transposed string representation of descriptive statistics.
            
        Returns:
            str: The interpolated prompt.
        """
        return f"""
You are an expert automated Data Profiling engine. Scan the structural profiles and descriptive matrices below to extract exactly 3 distinct, high-value data insights regarding trends, skewness, variations, or characteristics hidden within this dataset.

--- DATASET SUMMARY CONFIGURATIONS ---
Total Records: {metadata.get('total_records')}
Features Map: {metadata.get('columns')}
Statistical Summary Blocks:
{numeric_summary}

Provide your findings in a clear, bulleted summary format using bold highlights for crucial numbers. Focus on high-impact insights.

Automated Data Insights:
"""