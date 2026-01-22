from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from random import choice, random, seed
from typing import Sequence

from tqdm import tqdm

from constants import (ACTION_PROBABILITY, ACTIONS, DEFAULT_RANDOM_SEED,
                       ERROR_CODE_PROBABILITY, ERROR_CODES, LATENCIES_COUNT,
                       LATENCY_PROBABILITY, LEVELS, LOG_FILE, NUMBER_TEST_LOGS,
                       TIMESTAMP_FORMAT, USER_ID_PROBABILITY, USER_IDS_COUNT)
from fixtures import generate_latencies, generate_user_ids


def now_time() -> str:
    """Return current UTC time formatted for log records."""
    return datetime.now(timezone.utc).strftime(TIMESTAMP_FORMAT)


def create_log_line(
    latencies: Sequence[int],
    user_ids: Sequence[int],
) -> str:
    """Build one log line."""
    parts: list[str] = []
    level = choice(LEVELS)

    if random() < LATENCY_PROBABILITY:
        parts.append(f'latency_ms={choice(latencies)}')

    if random() < USER_ID_PROBABILITY:
        parts.append(f'user_id={choice(user_ids)}')

    if level in ('INFO', 'ERROR') and random() < ACTION_PROBABILITY:
        parts.append(f'action={choice(ACTIONS)}')

    if level == 'ERROR' and random() < ERROR_CODE_PROBABILITY:
        parts.append(f'code={choice(ERROR_CODES)}')

    return f'{now_time()} {level} {" ".join(parts)}'


def generate_log(
    out_file: Path,
    lines: int,
    random_seed: int | None = None,
    *,
    latencies_count: int = LATENCIES_COUNT,
    user_ids_count: int = USER_IDS_COUNT,
) -> None:
    """Generate a test log file with synthetic lines."""
    if random_seed is not None:
        seed(random_seed)

    latencies = generate_latencies(latencies_count)
    user_ids = generate_user_ids(user_ids_count)

    out_file.parent.mkdir(parents=True, exist_ok=True)

    with out_file.open('w', encoding='utf-8') as log:
        log.write(f'**** TEST LOG FILE | generated at {now_time()} ****\n\n')

        for _ in tqdm(range(lines), desc='Generating logs'):
            log.write(create_log_line(latencies, user_ids) + '\n')


if __name__ == '__main__':
    generate_log(
        out_file=LOG_FILE,
        lines=NUMBER_TEST_LOGS,
        random_seed=DEFAULT_RANDOM_SEED,
    )
