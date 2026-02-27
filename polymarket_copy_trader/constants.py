"""Application-wide constants."""

# Config
CONFIG_FILENAME = "config.json"

# Polymarket API
POLYMARKET_DATA_API_BASE_URL = "https://data-api.polymarket.com"

# Rate limiting (calls per period)
DEFAULT_RATE_LIMIT_CALLS = 25
RATE_LIMIT_PERIOD_SECONDS = 10

# Polling (detection latency: lower = faster but more API calls; keep under rate_limit)
POLL_INTERVAL_SECONDS = 0.5
MIN_POLL_INTERVAL_SECONDS = 0.3

# Order defaults (pmxt)
DEFAULT_ORDER_FEE_BPS = 1000
SIGNATURE_TYPE = 2

# Position comparison
POSITION_SIZE_EPSILON = 1e-9
