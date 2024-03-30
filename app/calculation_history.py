# calculation_history.py
import os
import pandas as pd
from dotenv import load_dotenv

class CalculationHistory:
    _instance = None

    #Code for implementing Singleton
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CalculationHistory, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance

    #Load environment variable and getting the absolute path of history_file path
    def initialize(self):
        load_dotenv()
        self.history_file = os.getenv('HISTORY_FILE_PATH', 'calculation_history.csv')
        self.history_file = os.path.abspath(self.history_file)
        self.history_df = self.load_or_initialize_history()

    #load the history_file path and read if csv file is present and if not create a datafram with one column 'Calculations'
    def load_or_initialize_history(self):
        #Look Before You Leap (LBYL)
        #Two fixed conditions whether the history_file path exists or not
        if os.path.exists(self.history_file):
            return pd.read_csv(self.history_file)
        else:
            return pd.DataFrame(columns=['Calculations'])

    #Add the calculation record by adding a new index in history dataframe and save it in csv file
    def add_record(self, operation, result):
        new_index = len(self.history_df)
        self.history_df.loc[new_index] = [operation]
        self.save_history()

    #save the record in history dataframe and in csv file. Check if the directory is present or not before saving
    def save_history(self):
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
        self.history_df.to_csv(self.history_file, index=False)

    #Load record history from csv file
    def load_history(self):
        #"Look Before You Leap" (LBYL)
        #Only two conditions whether history_file path exists or not
        if os.path.exists(self.history_file):
            self.history_df = pd.read_csv(self.history_file)
            return True
        return False

    #clear the record from history
    def clear_history(self):
        self.history_df = pd.DataFrame(columns=['Calculations'])
        self.save_history()

    #delete the record from history at a specific index
    def delete_history(self, index):
        #"Look Before You Leap" (LBYL)
        # we have higher chance that csv file may not be present or user might try to delete the record with an invalid index
        if not os.path.exists(self.history_file) or self.history_df.empty:
            return False  # Indicates no action was taken
        if index < 0 or index >= len(self.history_df):
            return False
        self.history_df = self.history_df.drop(index).reset_index(drop=True)
        self.save_history()
        return True