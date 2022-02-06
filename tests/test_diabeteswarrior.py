"""Tests for TDD"""
from diabeteswarrior import __version__


def test_version():
    """Application version"""
    assert __version__ == '0.1.0'
