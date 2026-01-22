import csv
import datetime as dt
from pathlib import Path
from typing import Any, Iterable

from prettytable import PrettyTable

from constants import CSV_DIR, FILENAME_TIMESTAMP_FORMAT


def fmt_count_pct(
        summary: dict[str, Any],
        level: str,
) -> str:
    """Format count and percentage for a log level."""
    cnt = summary.get(f'level_{level}', 0)
    pct = summary.get(f'level_{level}_pct')
    if pct is None:
        return str(cnt)
    return f'{cnt} ({pct}%)'


def print_summary_table(
        file_path: Path | str,
        summary: dict[str, Any],
) -> None:
    """Print a formatted summary table for a log file."""
    file_name = Path(file_path).name

    table = PrettyTable()
    table.title = f'Log summary for file: {file_name}'
    table.field_names = ['Metric', 'Value']
    table.align = {'Metric': 'l', 'Value': 'r'}

    groups = {
        'File': {
            'File path': file_path,
        },
        'Levels': {
            'ERROR': fmt_count_pct(summary, 'ERROR'),
            'WARNING': fmt_count_pct(summary, 'WARNING'),
            'INFO': fmt_count_pct(summary, 'INFO'),
        },
        'Latency': {
            'Count': summary.get('latency_count', 0),
            'Missing': summary.get('latency_missing', 0),
            'Sum (ms)': summary.get('latency_sum', 0),
            'Min (ms)': summary.get('min_latency'),
            'Max (ms)': summary.get('max_latency'),
        },
        'Errors': {
            'Total errors': summary.get('errors_total'),
        },
    }

    for group, items in groups.items():
        table.add_row([f'[{group}]', ''])
        for label, value in items.items():
            if value is not None:
                table.add_row([f'  {label}', value])

    print(table)


def file_output(
        results: Iterable[dict[str, Any]],
        file_path: Path | str,
) -> None:
    """Write summary results to a CSV file."""
    rows = list(results)
    if not rows:
        return

    CSV_DIR.mkdir(exist_ok=True)
    now = dt.datetime.now().strftime(FILENAME_TIMESTAMP_FORMAT)
    base_name = Path(file_path).stem
    out_file = CSV_DIR / f'{base_name}_{now}.csv'

    fieldnames = sorted({k for row in rows for k in row.keys()})

    with open(out_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f'CSV saved to: {out_file}')


def summary_to_csv_row(
        file_path: Path | str,
        summary: dict[str, Any],
) -> dict[str, Any]:
    """Convert a summary dict into a single CSV row."""
    row = {'file_path': str(file_path)}
    row.update(summary)
    return row
