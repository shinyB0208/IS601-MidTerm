# app/plugins/calculation/divide.py
from app.command.base_command import BaseCommand
from app.logging_utility import LoggingUtility

class DivideCommand(BaseCommand):

    def execute(self, *args):
        #"Easier to Ask for Forgiveness than Permission" (EAFP)
        #Instead of checking with multiple if else statement to check multiple error, it is easier to use try catch block
        try:
            if len(args) != 2:
                LoggingUtility.warning("Error: There can only be 2 arguments.")
                return
            dividend, divisor = map(float, args)
            result = dividend / divisor
            operation = " / ".join(args) + f" = {result}"
            self.history_instance.add_record(operation, result)
            LoggingUtility.info(result)
        except ValueError:
            LoggingUtility.error("Error: All arguments must be numbers.")
        except ZeroDivisionError:
            LoggingUtility.error("Error: Cannot divide by zero.")