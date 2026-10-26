"""
Advanced Python Rate Limiter
Algorithm: Token Bucket

Features:
- Configurable bucket capacity
- Configurable token refill rate
- Request allowance checks
- Retry-after calculation

Example:
Allow bursts of up to 5 requests, replenishing
1 token per second.
"""

import time


class TokenBucketRateLimiter:
    def __init__(self, capacity, refill_rate):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")

        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")

        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

    def _refill(self):
        """Add tokens according to elapsed time."""

        now = time.monotonic()
        elapsed = now - self.last_refill

        self.tokens = min(
            self.capacity,
            self.tokens + elapsed * self.refill_rate
        )

        self.last_refill = now

    def allow_request(self):
        """Return True if a request is allowed."""

        self._refill()

        if self.tokens >= 1:
            self.tokens -= 1
            return True

        return False

    def retry_after(self):
        """Return seconds until one token is available."""

        self._refill()

        if self.tokens >= 1:
            return 0.0

        return (1 - self.tokens) / self.refill_rate


# --------------------------------------------------
# Example Usage
# --------------------------------------------------

if __name__ == "__main__":

    # Capacity: 5 tokens
    # Refill: 1 token per second
    limiter = TokenBucketRateLimiter(
        capacity=5,
        refill_rate=1
    )

    # Simulate 7 immediate requests
    for request_id in range(1, 8):
        if limiter.allow_request():
            print(f"Request {request_id}: ALLOWED")
        else:
            print(
                f"Request {request_id}: RATE LIMITED "
                f"(retry after {limiter.retry_after():.2f}s)"
            )

    print("\nWaiting 1.1 seconds for token refill...")
    time.sleep(1.1)

    if limiter.allow_request():
        print("New request: ALLOWED")
    else:
        print("New request: RATE LIMITED")
