import contextlib
import time
from typing import Generator


@contextlib.contextmanager
def timing(name: str = "") -> Generator[None, None, None]:
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        elapsed = (end - start) * 1000
        unit = "ms"
        if elapsed < 100:
            elapsed *= 1000
            unit = "μs"
        if name:
            name = f" ({name})"
        print(f"> {int(elapsed)} {unit}{name}")
