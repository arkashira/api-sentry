import pytest
from api_sentry import ApiSentry, PerformanceMetric
from datetime import datetime

def test_add_metric():
    api_sentry = ApiSentry()
    metric = PerformanceMetric("endpoint1", 100.0, 200, datetime(2022, 1, 1))
    api_sentry.add_metric(metric)
    assert len(api_sentry.metrics) == 1

def test_get_historical_data():
    api_sentry = ApiSentry()
    metric1 = PerformanceMetric("endpoint1", 100.0, 200, datetime(2022, 1, 1))
    metric2 = PerformanceMetric("endpoint1", 200.0, 200, datetime(2022, 1, 2))
    metric3 = PerformanceMetric("endpoint2", 300.0, 200, datetime(2022, 1, 3))
    api_sentry.add_metric(metric1)
    api_sentry.add_metric(metric2)
    api_sentry.add_metric(metric3)
    historical_data = api_sentry.get_historical_data("endpoint1")
    assert len(historical_data) == 2

def test_get_trend_analysis():
    api_sentry = ApiSentry()
    metric1 = PerformanceMetric("endpoint1", 100.0, 200, datetime(2022, 1, 1))
    metric2 = PerformanceMetric("endpoint1", 200.0, 200, datetime(2022, 1, 2))
    api_sentry.add_metric(metric1)
    api_sentry.add_metric(metric2)
    trend_analysis = api_sentry.get_trend_analysis("endpoint1")
    assert trend_analysis["average_response_time"] == 150.0

def test_filter_metrics():
    api_sentry = ApiSentry()
    metric1 = PerformanceMetric("endpoint1", 100.0, 200, datetime(2022, 1, 1))
    metric2 = PerformanceMetric("endpoint1", 200.0, 200, datetime(2022, 1, 2))
    metric3 = PerformanceMetric("endpoint1", 300.0, 404, datetime(2022, 1, 3))
    api_sentry.add_metric(metric1)
    api_sentry.add_metric(metric2)
    api_sentry.add_metric(metric3)
    filtered_metrics = api_sentry.filter_metrics("endpoint1", 200)
    assert len(filtered_metrics) == 2

def test_sort_metrics():
    api_sentry = ApiSentry()
    metric1 = PerformanceMetric("endpoint1", 100.0, 200, datetime(2022, 1, 1))
    metric2 = PerformanceMetric("endpoint1", 200.0, 200, datetime(2022, 1, 2))
    metric3 = PerformanceMetric("endpoint1", 50.0, 200, datetime(2022, 1, 3))
    api_sentry.add_metric(metric1)
    api_sentry.add_metric(metric2)
    api_sentry.add_metric(metric3)
    sorted_metrics = api_sentry.sort_metrics("endpoint1", "response_time")
    assert sorted_metrics[0].response_time == 50.0
    assert sorted_metrics[1].response_time == 100.0
    assert sorted_metrics[2].response_time == 200.0

def test_sort_metrics_invalid_sort_by():
    api_sentry = ApiSentry()
    metric1 = PerformanceMetric("endpoint1", 100.0, 200, datetime(2022, 1, 1))
    with pytest.raises(ValueError):
        api_sentry.sort_metrics("endpoint1", "invalid_sort_by")
