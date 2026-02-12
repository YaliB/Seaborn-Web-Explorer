from .analysis_service import AnalysisServices
from .data_service import DataServices

data_service = DataServices("tips")
analysis_service = AnalysisServices(data_service)

data_service.load()