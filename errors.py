"""
Base error class for all PMT errors.

All custom errors extend this class to provide consistent error handling
across exchanges with HTTP status codes and retry semantics.
"""


class BaseError(Exception):
    """Base for all PMT exchange errors."""

    def __init__(
        self,
        message: str,
        status: int = 0,
        code: str = "ERROR",
        retryable: bool = False,
        exchange: str | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status = status
        self.code = code
        self.retryable = retryable
        self.exchange = exchange

    def __str__(self) -> str:
        return self.message


# ---------------------------------------------------------------------------
# 4xx Client Errors
# ---------------------------------------------------------------------------


class BadRequest(BaseError):
    """400 Bad Request - The request was malformed or contains invalid parameters."""

    def __init__(self, message: str, exchange: str | None = None) -> None:
        super().__init__(message, 400, "BAD_REQUEST", False, exchange)


class AuthenticationError(BaseError):
    """401 Unauthorized - Authentication credentials are missing or invalid."""

    def __init__(self, message: str, exchange: str | None = None) -> None:
        super().__init__(message, 401, "AUTHENTICATION_ERROR", False, exchange)


class PermissionDenied(BaseError):
    """403 Forbidden - The authenticated user doesn't have permission."""

    def __init__(self, message: str, exchange: str | None = None) -> None:
        super().__init__(message, 403, "PERMISSION_DENIED", False, exchange)


class NotFound(BaseError):
    """404 Not Found - The requested resource doesn't exist."""

    def __init__(self, message: str, exchange: str | None = None) -> None:
        super().__init__(message, 404, "NOT_FOUND", False, exchange)


class OrderNotFound(BaseError):
    """404 Not Found - The requested order doesn't exist."""

    def __init__(self, order_id: str, exchange: str | None = None) -> None:
        super().__init__(f"Order not found: {order_id}", 404, "ORDER_NOT_FOUND", False, exchange)


class MarketNotFound(BaseError):
    """404 Not Found - The requested market doesn't exist."""

    def __init__(self, market_id: str, exchange: str | None = None) -> None:
        super().__init__(f"Market not found: {market_id}", 404, "MARKET_NOT_FOUND", False, exchange)


class EventNotFound(BaseError):
    """404 Not Found - The requested event doesn't exist."""

    def __init__(self, identifier: str, exchange: str | None = None) -> None:
        super().__init__(f"Event not found: {identifier}", 404, "EVENT_NOT_FOUND", False, exchange)


class RateLimitExceeded(BaseError):
    """429 Too Many Requests - Rate limit exceeded."""

    def __init__(
        self,
        message: str,
        retry_after: int | None = None,
        exchange: str | None = None,
    ) -> None:
        super().__init__(message, 429, "RATE_LIMIT_EXCEEDED", True, exchange)
        self.retry_after = retry_after


class InvalidOrder(BaseError):
    """400 Bad Request - The order parameters are invalid."""

    def __init__(self, message: str, exchange: str | None = None) -> None:
        super().__init__(message, 400, "INVALID_ORDER", False, exchange)


class InsufficientFunds(BaseError):
    """400 Bad Request - Insufficient funds to complete the operation."""

    def __init__(self, message: str, exchange: str | None = None) -> None:
        super().__init__(message, 400, "INSUFFICIENT_FUNDS", False, exchange)


class ValidationError(BaseError):
    """400 Bad Request - Input validation failed."""

    def __init__(
        self,
        message: str,
        field: str | None = None,
        exchange: str | None = None,
    ) -> None:
        super().__init__(message, 400, "VALIDATION_ERROR", False, exchange)
        self.field = field


# ---------------------------------------------------------------------------
# 5xx Server/Network Errors
# ---------------------------------------------------------------------------


class NetworkError(BaseError):
    """503 Service Unavailable - Network connectivity issues (retryable)."""

    def __init__(self, message: str, exchange: str | None = None) -> None:
        super().__init__(message, 503, "NETWORK_ERROR", True, exchange)


class ExchangeNotAvailable(BaseError):
    """503 Service Unavailable - Exchange is down or unreachable (retryable)."""

    def __init__(self, message: str, exchange: str | None = None) -> None:
        super().__init__(message, 503, "EXCHANGE_NOT_AVAILABLE", True, exchange)
