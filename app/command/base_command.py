# app/command/base_command.py
from app.calculation_history import CalculationHistory

class BaseCommand:
    def __init__(self):
        self.history_instance = CalculationHistory()