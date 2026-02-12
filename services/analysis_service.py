import os
import pandas as pd
from services.data_service import DataServices
import matplotlib.pyplot as plt

class AnalysisServices:
    def __init__(self, data_service: DataServices):
        self.data_service = data_service
        
        self.plot_dir = os.path.join('static', 'plots')        
        if not os.path.exists(self.plot_dir):
            os.makedirs(self.plot_dir)
        
    def list_questions(self) -> list[dict]:
        raise NotImplementedError
    
    def run_question(self, questions_id: int) -> tuple[str, str, str]:
        """Return: (title, result_html, plot_path)"""
        match questions_id:
            case 1: 
                return ("Average tip by day", self.average_tip_by_day(), self.get_plot_path(1))
            case 2: 
                return ("Average total bill by time", self.average_total_bill_by_time(), self.get_plot_path(2))
            case 3: 
                return ("Tip percentage distribution", self.tip_percentage_distribution(), self.get_plot_path(3))
            case 4: 
                return ("Party size vs average tip", self.party_size_vs_average_tip(), self.get_plot_path(4))
            case 5: 
                return ("Smoker vs non-smoker: average tip", self.smoker_vs_non_smoker_average_tip(), self.get_plot_path(5))
        
        return "Unknown", self.data_service.get_df(), None
    
    def get_data_view(
        self,
        cols: str | None,
        filter_col: str | None,
        limit: int,
        op: str | None,
        value: str | None
    ) -> str:
        """Return HTML table string"""
        return self.data_service.get_df().head(limit).to_html()
        raise NotImplementedError
    
    
    
       
    
    def average_tip_by_day(self):
        return self.data_service.get_df().groupby("day")["tip"].mean().reset_index()

    def average_total_bill_by_time(self):
        return self.data_service.get_df().groupby("time")["total_bill"].mean().reset_index()


    def tip_percentage_distribution(self):
        df = self.data_service.get_df().copy() # to avoid SettingWithCopyWarning
        df["tip_pct"] = df["tip"] / df["total_bill"]
        
        mean_pct = df["tip_pct"].mean()
        median_pct = df["tip_pct"].median()
        
        #  to be able apply -to_html()
        result_df = pd.DataFrame({
            "Metric": ["Mean Tip Percentage", "Median Tip Percentage"],
            "Value": [mean_pct, median_pct]
        })
        
        return result_df

    def party_size_vs_average_tip(self):
        return self.data_service.get_df().groupby("size")["tip"].mean().reset_index()

    def smoker_vs_non_smoker_average_tip(self):
        return self.data_service.get_df().groupby("smoker")["tip"].mean().reset_index()
    
    
    
    def get_plot_path(self, q_id):
        """
        Creates a plot for a question by q_id and returns the image file path.
        """
        filename = f"plot_{q_id}.png"
        filepath = os.path.join('static', 'plots', filename)
        web_path = f"static/plots/{filename}"
        print(f"Checking if plot exists at: {filepath}")

        # If the plot already exists, return its path
        if os.path.exists(filepath):
            return web_path

        # Map q_id to the relevant analysis function
        analysis_funcs = {
            1: self.average_tip_by_day,
            2: self.average_total_bill_by_time,
            3: self.tip_percentage_distribution,
            4: self.party_size_vs_average_tip,
            5: self.smoker_vs_non_smoker_average_tip
        }

        func = analysis_funcs.get(q_id)
        if func is None:
            return None

        data = func()

        # Ensure the directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        plt.figure(figsize=(8, 5))

        # Generic plot logic based on columns
        if "day" in data.columns:
            data.plot(kind='bar', x='day', y='tip', color='skyblue', ax=plt.gca())
        elif "time" in data.columns:
            data.plot(kind='bar', x='time', y='total_bill', color='salmon', ax=plt.gca())
        elif "Metric" in data.columns:
            data.plot(kind='bar', x='Metric', y='Value', color='lightgreen', ax=plt.gca())
        elif "size" in data.columns:
            data.plot(kind='line', x='size', y='tip', marker='o', ax=plt.gca())
        elif "smoker" in data.columns:
            plt.pie(data['tip'], labels=data['smoker'], autopct='%1.1f%%')

        # Save and clear memory
        plt.savefig(filepath, bbox_inches='tight')
        plt.close()
        return web_path