# pylint: disable=protected-access
import os
import pandas as pd
import pytest
from app.calculation_history import CalculationHistory

@pytest.fixture
def mock_env(tmp_path, monkeypatch):
    # Create a temporary CSV file path
    temp_csv = tmp_path / "temp_calculation_history.csv"
    # Use monkeypatch to set environment variable to use the temp CSV path
    monkeypatch.setenv('HISTORY_FILE_PATH', str(temp_csv))
    return temp_csv

@pytest.fixture
def calculation_history_instance(mock_env):
    # Resetting _instance to ensure a fresh instance for each test
    CalculationHistory._instance = None
    return CalculationHistory()

def test_singleton_pattern(calculation_history_instance):
    instance_one = CalculationHistory()
    instance_two = CalculationHistory()
    assert instance_one is instance_two

def test_load_history_exists(calculation_history_instance, mock_env):
    # Pre-populate the CSV file with test data
    pd.DataFrame({"Calculations": ["2 + 2 = 4"]}).to_csv(mock_env, index=False)
    assert calculation_history_instance.load_history() is True
    assert not calculation_history_instance.history_df.empty

def test_load_history_not_exists(calculation_history_instance, mock_env):
    # Ensure the file does not exist by removing it if it does
    if mock_env.exists():
        os.remove(mock_env)
    assert calculation_history_instance.load_history() is False
    assert calculation_history_instance.history_df.empty

def test_add_record(calculation_history_instance):
    calculation_history_instance.add_record("3 + 3", 6)
    assert "3 + 3" in calculation_history_instance.history_df['Calculations'].values

def test_clear_history(calculation_history_instance):
    # Add a record to ensure the history is not initially empty
    calculation_history_instance.add_record("3 + 3", 6)
    calculation_history_instance.clear_history()
    assert calculation_history_instance.history_df.empty

def test_delete_history_valid_index(calculation_history_instance):
    calculation_history_instance.add_record("4 + 4", 8)
    calculation_history_instance.delete_history(0)
    assert calculation_history_instance.history_df.empty

def test_delete_history_invalid_index(calculation_history_instance):
    calculation_history_instance.add_record("4 + 4", 8)
    delete_status = calculation_history_instance.delete_history(10)  # Assuming an invalid index
    assert delete_status is False
    assert len(calculation_history_instance.history_df) == 1