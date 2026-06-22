import json
from dataclasses import dataclass
from typing import List

@dataclass
class Endpoint:
    url: str
    method: str

@dataclass
class Metric:
    endpoint: Endpoint
    response_time: float

class ApiSentry:
    def __init__(self):
        self.endpoints = []
        self.metrics = []

    def configure(self, endpoint: Endpoint):
        self.endpoints.append(endpoint)

    def collect_metrics(self, endpoint: Endpoint, response_time: float):
        metric = Metric(endpoint, response_time)
        self.metrics.append(metric)

    def get_metrics(self) -> List[Metric]:
        return self.metrics

    def detect_performance_degradation(self, threshold: float) -> List[Metric]:
        degraded_metrics = [metric for metric in self.metrics if metric.response_time > threshold]
        return degraded_metrics

    def send_alerts(self, degraded_metrics: List[Metric]):
        for metric in degraded_metrics:
            print(f"Alert: {metric.endpoint.url} is experiencing performance degradation with response time {metric.response_time} seconds")
