from pathlib import Path
from typing import Final

# CLI
OUTPUT_CHOICES: Final = ('table', 'csv')

# LOG GENERATOR SETTINGS
NUMBER_TEST_LOGS: Final = 100
DEFAULT_RANDOM_SEED: Final = 42
LATENCIES_COUNT: Final = 20
USER_IDS_COUNT: Final = 20
LATENCY_PROBABILITY: Final = 0.8
USER_ID_PROBABILITY: Final = 0.6
ACTION_PROBABILITY: Final = 0.7
ERROR_CODE_PROBABILITY: Final = 0.9

# FILE PATTERNS
FILE_PATTERNS: Final = ('*.log', '*.txt')

# PATHS
BASE_DIR: Final = Path(__file__).resolve().parent
LOG_DIR: Final = BASE_DIR / 'logs'
LOG_FILE: Final = LOG_DIR / 'app.log'
CSV_DIR: Final = BASE_DIR / 'results'

# LOG FORMAT
TIMESTAMP_FORMAT: Final = '%Y-%m-%d %H:%M:%S'
FILENAME_TIMESTAMP_FORMAT = "%Y-%m-%d_%H-%M-%S"

# DOMAIN CONSTANTS
SERVICE_ITEMS: Final = ('auth', 'payments', 'search')

ERROR_CODES: Final = (
    '401',
    '403',
    '404',
    '500',
    '502',
    'timeout',
    'db_error',
    'validation_failed',
    'unknown',
)

ACTIONS: Final = (
    'login',
    'logout',
    'search',
    'charge',
    'refund',
    'check_session',
)

LEVELS: Final = ('INFO', 'WARNING', 'ERROR')
