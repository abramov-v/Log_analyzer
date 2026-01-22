from typing import Any


def parse_line(
        log_line: str,
) -> dict[str, Any] | None:
    """Parse a log line into a structured record."""
    tokens = log_line.split()

    if len(tokens) < 3:
        return None

    fields = {}
    date, time_part, level = tokens[0], tokens[1], tokens[2]

    if level not in {'INFO', 'WARNING', 'ERROR'}:
        return None

    timestamp = f'{date} {time_part}'

    for token in tokens[3:]:
        if '=' not in token:
            continue

        key, value = token.split('=', 1)
        fields[key] = value

    return {
        'timestamp': timestamp,
        'level': level,
        'fields': fields,
        }
