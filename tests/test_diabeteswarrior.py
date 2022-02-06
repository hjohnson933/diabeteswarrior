"""Tests for TDD"""
from diabeteswarrior import __version__
from diabeteswarrior.calc_insulin_dose import main as cid
import diabeteswarrior.HLTH as Health

def test_version():
    """Application version"""
    assert __version__ == '0.1.0'

def test_insulin_dose():
    """Test for a insulin dose"""
    cid(act_bs=274) == "Bolus dose: 4, Basal dose: 2, Total dose: 6"


