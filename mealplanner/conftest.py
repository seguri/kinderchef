# https://pytest-django.readthedocs.io/en/latest/database.html#fixtures

import os
import pytest
from django.conf import settings
from django.core.management import call_command


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """
    Loads test data fixtures.

    From the docs I haven't fully understood why this function must be called exactly
    `django_db_setup` and why it needs the `django_db_setup` fixture to work.
    Every other variation simply doesn't work.
    """
    fixtures_dir = settings.BASE_DIR / "mealplanner" / "fixtures"
    with django_db_blocker.unblock():
        for filename in os.listdir(fixtures_dir):
            if filename.endswith(".json"):
                call_command("loaddata", str(fixtures_dir / filename))
