"""Tests for TDD"""
# pylint: disable=invalid-name

import arrow as A
import diabeteswarrior.HLTH as Health
from diabeteswarrior import __version__
from diabeteswarrior.calc_insulin_dose import main as cid


def test_version():
    """Application version"""
    assert __version__ == '0.1.0'

def test_health_version():
    """Test health version"""
    assert Health.__version__ == '0.1.0'

def test_insulin_dose():
    """Test for a insulin dose"""
    cdir = cid(act_bs=274)
    assert cdir == "Bolus dose: 4, Basal dose: 2, Total dose: 6"

def test_diabeteswarrior_health_record():
    """Test for correct health record."""
    r = {
        'po_pulse':88,
        'spox':97,
        'weight':135.5,
        'fat':6.5,
        'pulse':89,
        'systolic':160,
        'diastolic':81,
        'ihb':True,
        'hypertension':2,
        'temperature':97.9,
        't_s': A.now().format("YYYY-MM-DD HH:mm")
    }

    hr = Health.Records(**r)
    assert hr.po_pulse == r['po_pulse']
    assert hr.spox == r['spox']
    assert hr.weight == r['weight']
    assert hr.fat == r['fat']
    assert hr.pulse == r['pulse']
    assert hr.systolic == r['systolic']
    assert hr.diastolic == r['diastolic']
    assert hr.ihb == r['ihb']
    assert hr.hypertension == r['hypertension']
    assert hr.temperature == r['temperature']
    assert hr.t_s == r['t_s']
