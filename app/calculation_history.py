import pandas as pd

class CalculationHistory:
    def __init__(self, filepath='calculation_history.csv'):
        self.filepath = filepath
        self.history_df = pd.DataFrame(columns=['Operation', 'Result'])

    def load_history(self):
        try:
            self.history_df = pd.read_csv(self.filepath)
            print("History loaded.")
        except FileNotFoundError:
            print("No history found.")

    def save_history(self):
        self.history_df.to_csv(self.filepath, index=False)
        print("History saved.")

    def clear_history(self):
        self.history_df = pd.DataFrame(columns=['Operation', 'Result'])
        print("History cleared.")

    def delete_history(self, index):
        try:
            self.history_df = self.history_df.drop(index)
            self.save_history()
            print("Record deleted.")
        except KeyError:
            print("Invalid index for deletion.")