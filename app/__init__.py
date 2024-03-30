import os
import pkgutil
import importlib
import sys
from app.command import CommandHandler, Command
from dotenv import load_dotenv

class App:
    def __init__(self):
        load_dotenv()
        self.settings = self.load_environment_variables()
        self.settings.setdefault('ENVIRONMENT', 'PRODUCTION')
        self.command_handler = CommandHandler()

    def load_environment_variables(self):
        settings = {key: value for key, value in os.environ.items()}
        print("Environment variables loaded.")
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
        plugins_path = plugins_package.replace('.', '/')
        if not os.path.exists(plugins_path):
            print(f"Plugins directory '{plugins_path}' not found.")
            return
        for _, plugin_name, is_pkg in pkgutil.iter_modules([plugins_path]):
            if is_pkg:
                try:
                    plugin_module = importlib.import_module(f'{plugins_package}.{plugin_name}')
                    self.register_plugin_commands(plugin_module, plugin_name)
                except ImportError as e:
                    print(f"Error importing plugin {plugin_name}: {e}")

    def register_plugin_commands(self, plugin_module, plugin_name):
        for item_name in dir(plugin_module):
            item = getattr(plugin_module, item_name)
            if isinstance(item, type) and issubclass(item, Command) and item is not Command:
                # Command names are now explicitly set to the plugin's folder name
                self.command_handler.register_command(plugin_name, item())
                print(f"Command '{plugin_name}' from plugin '{plugin_name}' registered.")

    def start(self):
        self.load_plugins()
        self.show_menu()
        print("Application started. Type 'exit' to exit.")
        while True:
            input_line = input(">>> ").strip()
            if input_line == "":
                continue  # Skip empty input
            parts = input_line.split()  # Split input into parts by whitespace
            command_name = parts[0]
            args = parts[1:]  # All the remaining parts are considered arguments

        # Check if the command is 'menu' to show available commands
            if command_name == "menu":
                self.show_menu()
                continue

            try:
                self.command_handler.execute_command(command_name, *args)
            except KeyError:
                print(f"Unknown command: {command_name}")
                sys.exit(1)  # Use a non-zero exit code to indicate failure or incorrect command.