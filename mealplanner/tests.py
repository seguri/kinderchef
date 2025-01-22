import pytest
from django.contrib.auth import get_user_model

from mealplanner.models import DietaryRestriction


User = get_user_model()


# Create a fixture for one user object
@pytest.fixture
def admin():
    return User.objects.create_user("admin", "admin@example.com", "changeme")


@pytest.mark.django_db
def test_create_dietary_restriction(admin):
    restriction = DietaryRestriction.objects.create(
        name="Gluten", is_group=True, created_by=admin, updated_by=admin
    )
    restriction.save()


def inc(x):
    return x + 1


def test_inc():
    assert inc(3) == 4
