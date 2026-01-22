from random import randrange


def generate_latencies(count: int = 20) -> list[int]:
    """Generate sorted random latency values (20–299 ms)."""
    return sorted(randrange(20, 300) for _ in range(count))


def generate_user_ids(count: int = 20) -> list[int]:
    """Generate sorted random user IDs (1–59)."""
    return sorted(randrange(1, 60) for _ in range(count))
