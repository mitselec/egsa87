"""Allow running the package as a script: python -m egsa87."""

import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())
