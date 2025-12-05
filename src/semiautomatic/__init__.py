"""semiautomatic - Automation tools for creative AI workflows"""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("semiautomatic")
except PackageNotFoundError:
    __version__ = "0.0.0"  # Fallback for development without install