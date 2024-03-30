from app.command.base_command import BaseCommand
from app.logging_utility import LoggingUtility

class ClearCommand(BaseCommand):
    def execute(self, *args):
        #"Look Before You Leap" (LBYL)
        #We have only two conditions, also user might get confused if there are any arguements to be passed
        if len(args) > 0:
            LoggingUtility.warning("The clear command does not accept any arguments.")
        else:
            self.history_instance.clear_history()
            LoggingUtility.info("Calculation history cleared.")