import json
import os

def load_fixture(filename: str) -> dict:
    """Load a JSON fixture from the fixtures directory."""
    fixture_path = os.path.join(os.path.dirname(__file__), "..", "..", "fixtures", filename)
    with open(fixture_path, "r") as f:
        return json.load(f)