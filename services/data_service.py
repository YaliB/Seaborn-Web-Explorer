import pandas as pd
import seaborn as sns

class DataServices:
    def __init__(self, dataset_name: str):
        self.dataset_name = dataset_name
        self._df: pd.DataFrame | None = None
        
    def load(self) -> None:
        """Load dataset once on startup."""
        print(f"\n\n\n\nLoading dataset '{self.dataset_name}'...\n\n\n\n")
        self._df = sns.load_dataset(self.dataset_name)
        return None
    
    def get_df(self) -> pd.DataFrame:
        """Return cached DataFrame."""
        return self._df