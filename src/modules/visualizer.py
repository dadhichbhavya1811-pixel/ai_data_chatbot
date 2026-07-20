import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Optional
from src.utils.logger import setup_logger

logger = setup_logger("visualizer")

class DataVisualizer:
    """
    An Object-Oriented plotting module that transforms tabular Pandas DataFrames
    into interactive Plotly graphical visualization objects.
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Initializes the visualizer with a target dataset.
        
        Args:
            df (pd.DataFrame): Dataframe to visualize.
        """
        self.df = df

    def plot_bar(self, x_col: str, y_col: str, title: Optional[str] = None) -> go.Figure:
        """Generates an interactive Bar Chart."""
        logger.info(f"Generating Bar Chart: '{x_col}' vs '{y_col}'")
        fig = px.bar(self.df, x=x_col, y=y_col, title=title or f"{y_col} by {x_col}")
        fig.update_layout(template="plotly_white")
        return fig

    def plot_line(self, x_col: str, y_col: str, title: Optional[str] = None) -> go.Figure:
        """Generates an interactive Line Chart."""
        logger.info(f"Generating Line Chart: '{x_col}' vs '{y_col}'")
        fig = px.line(self.df, x=x_col, y=y_col, title=title or f"{y_col} Over {x_col}")
        fig.update_layout(template="plotly_white")
        return fig

    def plot_scatter(self, x_col: str, y_col: str, title: Optional[str] = None) -> go.Figure:
        """Generates an interactive Scatter Plot."""
        logger.info(f"Generating Scatter Plot: '{x_col}' vs '{y_col}'")
        fig = px.scatter(self.df, x=x_col, y=y_col, title=title or f"{y_col} vs {x_col}")
        fig.update_layout(template="plotly_white")
        return fig

    def plot_histogram(self, col: str, bins: int = 30, title: Optional[str] = None) -> go.Figure:
        """Generates an interactive Histogram distribution chart."""
        logger.info(f"Generating Histogram for column: '{col}'")
        fig = px.histogram(self.df, x=col, nbins=bins, title=title or f"Distribution of {col}")
        fig.update_layout(template="plotly_white")
        return fig

    def plot_boxplot(self, y_col: str, x_col: Optional[str] = None, title: Optional[str] = None) -> go.Figure:
        """Generates an interactive Box Plot to view distribution and statistical outliers."""
        logger.info(f"Generating Box Plot for attribute: '{y_col}'")
        fig = px.box(self.df, x=x_col, y=y_col, title=title or f"Statistical Spread of {y_col}")
        fig.update_layout(template="plotly_white")
        return fig

    def plot_correlation_heatmap(self, corr_matrix: pd.DataFrame) -> go.Figure:
        """
        Generates a graphical structural representation of a correlation matrix.
        
        Args:
            corr_matrix (pd.DataFrame): Calculated Pearson correlation matrix.
            
        Returns:
            go.Figure: Correlation heat-map plot.
        """
        logger.info("Generating linear Pearson Correlation Heatmap chart...")
        if corr_matrix.empty:
            # Fallback plot if matrix doesn't contain entries
            fig = go.Figure()
            fig.update_layout(title="No numerical correlation data available.")
            return fig
            
        fig = px.imshow(
            corr_matrix,
            text_auto=".2f",
            color_continuous_scale="RdBu_r",
            title="Variable Linear Correlation Analysis",
            aspect="auto"
        )
        return fig