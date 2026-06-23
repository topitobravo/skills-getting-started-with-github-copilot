import pytest
from copy import deepcopy
from fastapi.testclient import TestClient

from src.app import app, activities as _activities

# Backup the original activities state to restore between tests
_backup = deepcopy(_activities)


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Autouse fixture to reset the in-memory `activities` before each test.

    Uses a deep copy of the original backup to avoid shared references.
    """
    _activities.clear()
    _activities.update(deepcopy(_backup))
    yield
    _activities.clear()
    _activities.update(deepcopy(_backup))
