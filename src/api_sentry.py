import json
from dataclasses import dataclass
from typing import Optional
from unittest.mock import patch

@dataclass
class ProviderStatus:
    outage: bool
    link: Optional[str]
    eta: Optional[str]

def get_provider_status() -> ProviderStatus:
    # Simulate provider status API query
    return ProviderStatus(outage=True, link="https://example.com/outage", eta="1 hour")

def diagnose_error_rate(error_rate: float, duration: int) -> str:
    if error_rate > 10 and duration >= 5:
        status = get_provider_status()
        if status.outage:
            return f"Provider outage detected. Link: {status.link}, ETA: {status.eta}"
        else:
            return "No provider outage detected. Check quota limits."
    else:
        return "Error rate is not high enough to trigger diagnosis."

def main():
    error_rate = 15.0
    duration = 10
    print(diagnose_error_rate(error_rate, duration))

if __name__ == "__main__":
    main()
