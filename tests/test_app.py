import os
import pytest
from app import App

def test_app_start_exit_command(capfd, monkeypatch):
    """Test that the REPL exits correctly on 'exit' command."""
    # Simulate user entering 'exit'
    monkeypatch.setattr('builtins.input', lambda _: 'exit')
    app = App()
    with pytest.raises(SystemExit) as e:
        app.start()
    assert e.type == SystemExit

def test_app_start_unknown_command(capfd, monkeypatch):
    """Test how the REPL handles an unknown command before exiting."""
    # Simulate user entering an unknown command followed by 'exit'
    inputs = iter(['unknown_command', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    app = App()

    with pytest.raises(SystemExit) as excinfo:
        app.start()

    # Optionally, check for specific exit code or message
    # assert excinfo.value.code == expected_exit_code

    # Verify that the unknown command was handled as expected
    captured = capfd.readouterr()
    assert "No such command: unknown_command" in captured.out

def test_load_environment_variables():
    app = App()
    # Assuming you have set 'ENVIRONMENT' in your .env or during testing setup
    environment = app.get_environment_variable('ENVIRONMENT')
    assert environment is not None
    assert environment == 'PRODUCTION'  # Or whatever you expect it to be

def test_plugin_loading(monkeypatch):
    # Mock the os.environ.get to return a specific plugin
    monkeypatch.setattr(os, 'environ', {'ENABLED_PLUGINS': 'add,subtract'})
    app = App()
    app.load_plugins()
    # Ensure that the expected plugins are loaded and registered
    assert 'add' in app.command_handler.commands
    assert 'subtract' in app.command_handler.commands

def test_empty_input(capfd, monkeypatch):
    inputs = iter(['', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    app = App()
    with pytest.raises(SystemExit):
        app.start()
    captured = capfd.readouterr()
    # Check for any unwanted output or behavior, or simply ensure it doesn't crash