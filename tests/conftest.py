# Ensure the project root is on sys.path when running tests via pytest.
# This allows importing top-level modules (like api_client) from test modules.

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
