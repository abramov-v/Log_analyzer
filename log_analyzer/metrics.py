from typing import Any


def create_summary() -> dict:
    """Create an empty metrics summary structure."""
    return {
        'total_lines': 0,
        'parsed_ok': 0,
        'parsed_failed': 0,

        'level_INFO': 0,
        'level_WARNING': 0,
        'level_ERROR': 0,
        'errors_total': 0,

        'latency_missing': 0,
        'latency_invalid': 0,
        'latency_count': 0,
        'latency_sum': 0,
        'min_latency': None,
        'max_latency': None,
    }


def process_record(
        record: dict[str, Any] | None,
        metrics_state: dict,
) -> None:
    """Update metrics summary with a single parsed log record."""
    metrics_state['total_lines'] += 1

    if record is None:
        metrics_state['parsed_failed'] += 1
        return

    metrics_state['parsed_ok'] += 1

    level = record.get('level')

    if level:
        metrics_state[f'level_{level}'] += 1

    if level == 'ERROR':
        metrics_state['errors_total'] += 1

    fields = record.get('fields', {})

    if 'latency_ms' not in fields:
        metrics_state['latency_missing'] += 1
        return

    try:
        latency_value = int(fields['latency_ms'])
    except (TypeError, ValueError):
        metrics_state['latency_invalid'] += 1
        return

    metrics_state['latency_count'] += 1
    metrics_state['latency_sum'] += latency_value

    if metrics_state['min_latency'] is None:
        metrics_state['min_latency'] = latency_value
    else:
        metrics_state['min_latency'] = min(metrics_state['min_latency'], latency_value)

    if metrics_state['max_latency'] is None:
        metrics_state['max_latency'] = latency_value
    else:
        metrics_state['max_latency'] = max(metrics_state['max_latency'], latency_value)


def finalise_summary(
        summary: dict,
        base_key: str = 'parsed_ok',
) -> None:
    """Calculate percentage metrics based on parsed records."""
    base = summary.get(base_key, 0)
    if base == 0:
        return

    for level in ('ERROR', 'WARNING', 'INFO'):
        count = summary.get(f'level_{level}', 0)
        summary[f'level_{level}_pct'] = round(count / base * 100)
