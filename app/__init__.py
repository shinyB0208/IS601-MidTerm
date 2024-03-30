import os
import pkgutil
import importlib
import sys
from app.command import CommandHandler, Command
from dotenv import load_dotenv
from app.logging_utility import LoggingUtility

class App:
    def __init__(self):
        LoggingUtility.configure_logging()
        load_dotenv()
        self.settings = self.load_environment_variables()
        self.settings.setdefault('ENVIRONMENT', 'PRODUCTION')
        self.command_handler = CommandHandler()

    def load_environment_variables(self):
        settings = {key: value for key, value in os.environ.items()}
        LoggingUtility.info("Environment variables loaded.")
        return settings

    def get_environment_variable(self, env_var: str = 'ENVIRONMENT'):
        return self.settings.get(env_var, None)
            
    def show_menu(self):
        print("Available commands:")
        # List all registered commands
        for command_name in self.command_handler.commands.keys():
            print(f"- {command_name}")

    def load_plugins(self):
        plugins_package = 'app.plugins'
        calculation_path = os.path.join(plugins_package.replace('.', '/'), 'calculations')
        history_path = os.path.join(plugins_package.replace('.', '/'), 'history')
        other_plugins_path = plugins_package.replace('.', '/')
        
        self.load_plugin_commands(calculation_path, f'{plugins_package}.calculations')
        self.load_plugin_commands(history_path, f'{plugins_package}.history')
        
        self.load_plugin_commands(other_plugins_path,f'{plugins_package}')
               
    def load_plugin_commands(self, path, package):
        if not os.path.exists(path):
            LoggingUtility.warning(f"Directory '{path}' not found.")
            return
        for _, plugin_name, _ in pkgutil.iter_modules([path]):
            #"Easier to Ask for Forgiveness than Permission" (EAFP)
            #Very few chance of getting the import error
            try:
                plugin_module = importlib.import_module(f'{package}.{plugin_name}')
                command_instance = getattr(plugin_module, f'{plugin_name.capitalize()}Command')()
                self.command_handler.register_command(plugin_name, command_instance)
                LoggingUtility.info(f"Command '{plugin_name}' from plugin '{plugin_name}' registered.")
            except ImportError as e:
                LoggingUtility.error(f"Error importing plugin {plugin_name}: {e}")

        

    def register_plugin_commands(self, plugin_module, plugin_name):
        for item_name in dir(plugin_module):
            item = getattr(plugin_module, item_name)
            if isinstance(item, type) and issubclass(item, Command) and item is not Command:
                self.command_handler.register_command(plugin_name, item())
                LoggingUtility.info(f"Command '{plugin_name}' from plugin '{plugin_name}' registered.")

     #initiates a Read-Eval-Print Loop (REPL), continuously accepting user input. 
    def start(self):
        self.load_plugins()
        self.show_menu()
        LoggingUtility.info("Application started. Type 'exit' to exit.")
        while True:
            input_line = input(">>> ").strip()
            if input_line == "":
                continue
            parts = input_line.split()
            command_name = parts[0]
            args = parts[1:]

            if command_name == "menu":
                self.show_menu()
                continue
            
            #"Easier to Ask for Forgiveness than Permission" (EAFP)
            #Very few chance of getting an unknown command error
            try:
                self.command_handler.execute_command(command_name, *args)
            except KeyError:
                LoggingUtility.error(f"Unknown command: {command_name}")
                sys.exit(1)