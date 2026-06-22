import json
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict

@dataclass
class PerformanceMetric:
    endpoint: str
    response_time: float
    status_code: int
    timestamp: datetime

class ApiSentry:
    def __init__(self):
        self.metrics = []

    def add_metric(self, metric: PerformanceMetric):
        self.metrics.append(metric)

    def get_historical_data(self, endpoint: str) -> List[PerformanceMetric]:
        return [metric for metric in self.metrics if metric.endpoint == endpoint]

    def get_trend_analysis(self, endpoint: str) -> Dict[str, float]:
        metrics = self.get_historical_data(endpoint)
        if not metrics:
            return {}
        response_times = [metric.response_time for metric in metrics]
        average_response_time = sum(response_times) / len(response_times)
        return {"average_response_time": average_response_time}

    def filter_metrics(self, endpoint: str, status_code: int) -> List[PerformanceMetric]:
        return [metric for metric in self.metrics if metric.endpoint == endpoint and metric.status_code == status_code]

    def sort_metrics(self, endpoint: str, sort_by: str) -> List[PerformanceMetric]:
        metrics = self.get_historical_data(endpoint)
        if sort_by == "response_time":
            return sorted(metrics, key=lambda x: x.response_time)
        elif sort_by == "timestamp":
            return sorted(metrics, key=lambda x: x.timestamp)
        else:
            raise ValueError("Invalid sort_by parameter")
