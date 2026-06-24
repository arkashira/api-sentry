import json
from dataclasses import dataclass

@dataclass
class ApiSentryConfig:
    license: str
    status: str

class ApiSentry:
    def __init__(self, config: ApiSentryConfig):
        self.config = config

    def get_badges(self):
        return {
            "License": self.config.license,
            "Status": self.config.status
        }

    def get_features(self):
        return [
            {"Feature": "Feature 1", "Description": "Description 1"},
            {"Feature": "Feature 2", "Description": "Description 2"}
        ]

    def get_why_api_sentry(self):
        return [
            "Reason 1",
            "Reason 2",
            "Reason 3",
            "Reason 4",
            "Reason 5"
        ]

    def get_project_structure(self):
        return {
            "src": ["api_sentry.py"],
            "tests": ["test_api_sentry.py"],
            "README.md": []
        }

    def get_getting_started(self):
        return "Getting started with api-sentry"
