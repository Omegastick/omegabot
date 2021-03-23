import pytest
from omegabot.models import ALL_MODELS
from playhouse.sqlite_ext import SqliteExtDatabase


@pytest.fixture(scope="function", autouse=True)
def test_database():
    test_db = SqliteExtDatabase(":memory:")
    with test_db.bind_ctx(ALL_MODELS):
        test_db.create_tables(ALL_MODELS)
        try:
            yield
        finally:
            test_db.drop_tables(ALL_MODELS)
            test_db.close()
