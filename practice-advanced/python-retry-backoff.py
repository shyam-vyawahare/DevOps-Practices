"""
Advanced Python Retry with Exponential Backoff
DevOps Practice

Features:
- Configurable maximum attempts
- Exponential delay between retries
- Random jitter to avoid synchronized retries
- Retryable exception handling
- Optional maximum delay

Note:
Use retries for transient failures, not permanent errors.
"""

import random
import time
from functools import wraps


def retry(
    max_attempts=5,
    base_delay=1.0,
    max_delay=30.0,
    jitter=True,
    exceptions=(Exception,)
):
    """Retry a function using exponential backoff."""

    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")

    if base_delay < 0 or max_delay < 0:
        raise ValueError("Delays must be non-negative")

    if not exceptions or not all(
        isinstance(exc, type) and issubclass(exc, Exception)
        for exc in exceptions
    ):
        raise ValueError("exceptions must contain exception classes")

    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return function(*args, **kwargs)

                except exceptions:
                    if attempt == max_attempts:
                        print(f"Failed after {max_attempts} attempts.")
                        raise

                    delay = min(
                        max_delay,
                        base_delay * (2 ** (attempt - 1))
                    )

                    if jitter:
                        delay = random.uniform(0, delay)

                    print(
                        f"Attempt {attempt} failed. "
                        f"Retrying in {delay:.2f} seconds..."
                    )

                    time.sleep(delay)

        return wrapper

    return decorator


# --------------------------------------------------
# Example Usage
# --------------------------------------------------

attempt_counter = 0


@retry(
    max_attempts=4,
    base_delay=1,
    max_delay=5,
    jitter=True,
    exceptions=(ConnectionError,)
)
def call_unstable_service():
    """Simulate a service that temporarily fails."""

    global attempt_counter
    attempt_counter += 1

    print(f"Calling service (attempt {attempt_counter})...")

    if attempt_counter < 3:
        raise ConnectionError("Temporary service failure")

    return "Service request successful!"


if __name__ == "__main__":
    try:
        result = call_unstable_service()
        print(result)

    except ConnectionError as error:
        print(f"Service unavailable: {error}")
