import os
import pkgutil
import importlib
from app.command import CommandHandler,Command
from app.command.menu_command import MenuCommand
from dotenv import load_dotenv

class App:
    def __init__(self):
        load_dotenv()
        self.settings = self.load_environment_variables()
        self.settings.setdefault('ENVIRONMENT', 'PRODUCTION')
        self.command_handler = CommandHandler()
        self.load_commands()

    def load_environment_variables(self):
        settings = {key: value for key, value in os.environ.items()}
        return settings

    def get_environment_variable(self, env_var: str = 'ENVIRONMENT'):
        return self.settings.get(env_var, None)

    def load_commands(self):
        enabled_plugins = os.getenv('ENABLED_PLUGINS', '').split(',')

        # Dynamically load plugins
        plugins_package = 'app.plugins'
        for _, plugin_name, _ in pkgutil.iter_modules(['app/plugins']):
            if plugin_name in enabled_plugins:
                plugin_module = importlib.import_module(f'{plugins_package}.{plugin_name}')
                command_class = getattr(plugin_module, f'{plugin_name.capitalize()}Command')
                self.command_handler.register_command(plugin_name, command_class())

        # Register MenuCommand
        self.command_handler.register_command("menu", MenuCommand(self.command_handler))

    def start(self):
        print("Type 'menu' to see available commands. Type 'exit' to exit.")
        while True:
            command_input = input(">>> ").strip()
            if command_input == "exit":
                break
            if command_input:
                command_name, *args = command_input.split()
                self.command_handler.execute_command(command_name, *args)