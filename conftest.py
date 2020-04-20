import pytest

import geocoding


@pytest.fixture
def addresses():
    rows = geocoding.collect_rows()
    return rows
