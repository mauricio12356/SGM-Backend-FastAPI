import os
from pathlib import Path

TEST_DB = Path(__file__).parent / "test_sgm.db"
if TEST_DB.exists():
    TEST_DB.unlink()
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB}"
os.environ["DEFAULT_ADMIN_EMAIL"] = "admin@test.local"
os.environ["DEFAULT_ADMIN_PASSWORD"] = "Admin123*"
