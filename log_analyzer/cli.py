import argparse
from pathlib import Path

from constants import OUTPUT_CHOICES
from metrics import create_summary, finalise_summary, process_record
from parsing import parse_line
from reader import find_log_files, read_files
from utils import file_output, print_summary_table, summary_to_csv_row


def configure_argument_parser() -> argparse.ArgumentParser:
    """Configure and return the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description='Parse log files and output summary metrics.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        '-p', '--path',
        type=Path,
        required=True,
        help=(
            'Path to a log file or directory with logs.\n'
            'Example (Windows): "X:\\...\\logs" or "X:/.../logs"'
        ),
    )

    parser.add_argument(
        '-o', '--output',
        choices=OUTPUT_CHOICES,
        default='table',
        help='Output format',
    )

    return parser


def main() -> None:
    """Run log analysis from the command line."""
    args = configure_argument_parser().parse_args()
    summaries_by_file = {}

    files = list(find_log_files(args.path))
    if not files:
        print('No log files found')
        return

    for file_path in files:
        summary = create_summary()
        for line in read_files(file_path):
            record = parse_line(line)
            process_record(record, summary)
        finalise_summary(summary)
        summaries_by_file[str(file_path)] = summary

    if args.output == 'table':
        for file_path, summary in summaries_by_file.items():
            print_summary_table(file_path, summary)

    elif args.output == 'csv':
        csv_rows = [
            summary_to_csv_row(file_path, summary)
            for file_path, summary in summaries_by_file.items()
        ]
        if csv_rows:
            path = Path(args.path).name
            file_output(csv_rows, path)


if __name__ == '__main__':
    main()
