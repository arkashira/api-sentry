import pytest
from api_sentry import ApiSentry, ApiSentryConfig

def test_api_sentry_config():
    config = ApiSentryConfig(license="MIT", status="In Development")
    assert config.license == "MIT"
    assert config.status == "In Development"

def test_api_sentry_get_badges():
    config = ApiSentryConfig(license="MIT", status="In Development")
    api_sentry = ApiSentry(config)
    badges = api_sentry.get_badges()
    assert badges["License"] == "MIT"
    assert badges["Status"] == "In Development"

def test_api_sentry_get_features():
    config = ApiSentryConfig(license="MIT", status="In Development")
    api_sentry = ApiSentry(config)
    features = api_sentry.get_features()
    assert len(features) == 2
    assert features[0]["Feature"] == "Feature 1"
    assert features[0]["Description"] == "Description 1"
    assert features[1]["Feature"] == "Feature 2"
    assert features[1]["Description"] == "Description 2"

def test_api_sentry_get_why_api_sentry():
    config = ApiSentryConfig(license="MIT", status="In Development")
    api_sentry = ApiSentry(config)
    why_api_sentry = api_sentry.get_why_api_sentry()
    assert len(why_api_sentry) == 5
    assert why_api_sentry[0] == "Reason 1"
    assert why_api_sentry[1] == "Reason 2"
    assert why_api_sentry[2] == "Reason 3"
    assert why_api_sentry[3] == "Reason 4"
    assert why_api_sentry[4] == "Reason 5"

def test_api_sentry_get_project_structure():
    config = ApiSentryConfig(license="MIT", status="In Development")
    api_sentry = ApiSentry(config)
    project_structure = api_sentry.get_project_structure()
    assert project_structure["src"] == ["api_sentry.py"]
    assert project_structure["tests"] == ["test_api_sentry.py"]
    assert project_structure["README.md"] == []

def test_api_sentry_get_getting_started():
    config = ApiSentryConfig(license="MIT", status="In Development")
    api_sentry = ApiSentry(config)
    getting_started = api_sentry.get_getting_started()
    assert getting_started == "Getting started with api-sentry"
