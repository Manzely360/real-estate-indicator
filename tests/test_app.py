import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from roi import calculate_roi


def test_calculate_roi_basic():
    roi = calculate_roi(100000, 10000, 12000, 2000)
    assert round(roi, 2) == 9.09


def test_calculate_roi_zero_investment():
    roi = calculate_roi(0, 0, 1000, 500)
    assert roi == 0
