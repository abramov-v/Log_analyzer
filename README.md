# Log files analyzer

A CLI utility for analyzing log files and producing aggregated metrics (log levels, errors, latency statistics, etc.).

The tool includes:
- a test log generator
- a log analyzer
- a command-line interface (CLI)
- output in table or CSV format

## Startup instructions

1. Clone the repository and navigate to it in the command line:

```bash
git clone git@github.com:abramov-v/log_analyzer.git
cd log_analyzer
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Generate test logs:

```bash
python log_generator.py
```

This will generate a test log file in the `logs/` directory.

## CLI Usage

1. Print summary table

```bash
python cli.py --path path/to/logs --output table
```

2. Export summary to CSV file

```bash
python cli.py --path path/to/logs --output csv
```

CSV files are saved to the `results/` directory.


## Log format - example

```
2026-01-22 22:04:19 WARNING latency_ms=134
2026-01-22 22:04:19 INFO latency_ms=278 user_id=29 action=search
2026-01-22 22:04:19 ERROR latency_ms=134 user_id=7 action=logout code=403
2026-01-22 22:04:19 INFO user_id=45 action=search
2026-01-22 22:04:19 ERROR latency_ms=131 code=401
```

## Example Output (Table)

```
+---------------------------------------------------------------------------------------+
|                             Log summary for file: app.log                             |
+----------------+----------------------------------------------------------------------+
| Metric         |                                                                Value |
+----------------+----------------------------------------------------------------------+
| [File]         |                                                                      |
|   File path    | path/to/logs/                                                        |
| [Levels]       |                                                                      |
|   ERROR        |                                                             33 (33%) |
|   WARNING      |                                                             28 (28%) |
|   INFO         |                                                             39 (39%) |
| [Latency]      |                                                                      |
|   Count        |                                                                   81 |
|   Missing      |                                                                   19 |
|   Sum (ms)     |                                                                11257 |
|   Min (ms)     |                                                                   32 |
|   Max (ms)     |                                                                  299 |
| [Errors]       |                                                                      |
|   Total errors |                                                                   33 |
+----------------+----------------------------------------------------------------------+
```