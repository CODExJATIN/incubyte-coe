from pathlib import Path

import pytest

from order_cleaner import clean_file


@pytest.fixture
def clean_sample_csv(tmp_path):
    clean_path = tmp_path / "clean.csv"
    clean_file(Path(__file__).parent / "orders.csv", clean_path)
    return clean_path
