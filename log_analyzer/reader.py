import fnmatch
from pathlib import Path
from typing import Iterable

from constants import FILE_PATTERNS


def find_log_files(
        path: Path,
        patterns: tuple[str, ...] = FILE_PATTERNS,
) -> Iterable[Path]:
    """Yield log files matching patterns from a file or directory."""
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f'Path does not exist: {path}')

    if path.is_file():
        if any(fnmatch.fnmatch(path.name, p) for p in patterns):
            yield path
        return

    for p in patterns:
        yield from sorted(path.rglob(p))


def read_files(
        file_path: Path
) -> Iterable[str]:
    """Yield non-empty log lines from a file, skipping header lines."""
    with open(file_path, 'r', encoding='utf-8') as f:
        first = next(f, None)
        if first is not None:
            first = first.strip()
            if first and not first.startswith('****'):
                yield first

        for line in f:
            line = line.strip()
            if line:
                yield line
