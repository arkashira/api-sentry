import pytest
from unittest.mock import patch
from api_sentry import diagnose_error_rate, get_provider_status, ProviderStatus

def test_diagnose_error_rate_high_error_rate():
    error_rate = 15.0
    duration = 10
    result = diagnose_error_rate(error_rate, duration)
    assert "Provider outage detected" in result

def test_diagnose_error_rate_low_error_rate():
    error_rate = 5.0
    duration = 10
    result = diagnose_error_rate(error_rate, duration)
    assert result == "Error rate is not high enough to trigger diagnosis."

def test_diagnose_error_rate_no_outage():
    error_rate = 15.0
    duration = 10
    # Simulate no outage
    with patch('api_sentry.get_provider_status') as mock_get_provider_status:
        mock_get_provider_status.return_value = ProviderStatus(outage=False, link=None, eta=None)
        result = diagnose_error_rate(error_rate, duration)
        assert "No provider outage detected" in result

def test_get_provider_status():
    status = get_provider_status()
    assert status.outage
    assert status.link
    assert status.eta
