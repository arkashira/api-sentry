from api_sentry import ApiSentry, Endpoint, Metric
import pytest

def test_configure():
    api_sentry = ApiSentry()
    endpoint = Endpoint("https://example.com", "GET")
    api_sentry.configure(endpoint)
    assert endpoint in api_sentry.endpoints

def test_collect_metrics():
    api_sentry = ApiSentry()
    endpoint = Endpoint("https://example.com", "GET")
    api_sentry.configure(endpoint)
    api_sentry.collect_metrics(endpoint, 0.5)
    assert len(api_sentry.get_metrics()) == 1

def test_get_metrics():
    api_sentry = ApiSentry()
    endpoint = Endpoint("https://example.com", "GET")
    api_sentry.configure(endpoint)
    api_sentry.collect_metrics(endpoint, 0.5)
    metrics = api_sentry.get_metrics()
    assert len(metrics) == 1
    assert metrics[0].endpoint == endpoint
    assert metrics[0].response_time == 0.5

def test_detect_performance_degradation():
    api_sentry = ApiSentry()
    endpoint = Endpoint("https://example.com", "GET")
    api_sentry.configure(endpoint)
    api_sentry.collect_metrics(endpoint, 1.0)
    degraded_metrics = api_sentry.detect_performance_degradation(0.5)
    assert len(degraded_metrics) == 1
    assert degraded_metrics[0].endpoint == endpoint
    assert degraded_metrics[0].response_time == 1.0

def test_send_alerts():
    api_sentry = ApiSentry()
    endpoint = Endpoint("https://example.com", "GET")
    api_sentry.configure(endpoint)
    api_sentry.collect_metrics(endpoint, 1.0)
    degraded_metrics = api_sentry.detect_performance_degradation(0.5)
    api_sentry.send_alerts(degraded_metrics)
    # No assertion, just test that it runs without error

def test_edge_case_empty_endpoints():
    api_sentry = ApiSentry()
    assert len(api_sentry.endpoints) == 0

def test_edge_case_empty_metrics():
    api_sentry = ApiSentry()
    assert len(api_sentry.get_metrics()) == 0
