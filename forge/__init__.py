"""Metapackage bundling qwen-think and qwen3.6-mtp under a shared namespace."""

from . import mtp, session  # noqa: F401

__version__ = "0.1.0"

__all__ = [
    "session",
    "mtp",
]
