from app.command.base_command import BaseCommand
from app.logging_utility import LoggingUtility

class LoadCommand(BaseCommand):
    def execute(self):
        success = self.history_instance.load_history()
        #"Look Before You Leap" (LBYL)
        #We have fixed condition whether history can be loaded or not and if csv file is empty or not. High chance of getting errors
        if success:
            if not self.history_instance.history_df.empty:
                LoggingUtility.info(self.history_instance.history_df.to_string(index=False))
            else:
                LoggingUtility.warning("No calculations in history.")
        else:
            LoggingUtility.warning("Unable to load history. No CSV file present.")