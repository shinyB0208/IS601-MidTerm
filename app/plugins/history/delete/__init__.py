from app.command.base_command import BaseCommand
from app.logging_utility import LoggingUtility

class DeleteCommand(BaseCommand):
    def execute(self, *args):
        #"Look Before You Leap" (LBYL)
        #We have one arguement to be passed for delete command, high chance that user might pass more than one arguement
        if len(args) == 0:
            LoggingUtility.warning("You have to declare an index after the delete command.")
        elif len(args) > 1:
            LoggingUtility.warning("You can declare only one index after the delete command.")
        else:
            try:
                #"Easier to Ask for Forgiveness than Permission" (EAFP)
                #Instead of checking with multiple if else statement to check multiple error, it is easier to use try catch block
                index = int(args[0])
                # Proceed with deletion if the provided index is valid
                if not self.history_instance.delete_history(index - 1):  # Adjusting index to be 0-based
                    LoggingUtility.warning("Unable to delete record. Please check the index or CSV file.")
                else:
                    LoggingUtility.info("Record deleted.")
            except ValueError:
                LoggingUtility.error("Error: Index must be an integer.")