import pytest
from app import App

@pytest.fixture
def app_instance():
    """Fixture to create an app instance."""
    return App()