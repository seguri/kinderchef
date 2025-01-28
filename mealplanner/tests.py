from datetime import date, datetime
from zoneinfo import ZoneInfo

import pytest
from dateutil.rrule import rrulestr

from mealplanner.models import (
    Child,
    DietaryRestriction,
    Meal,
    to_aware_datetime,
    to_naive_datetime,
)


@pytest.mark.django_db
def test_muhammad_ali_is_muslim():
    ali = Child.objects.get(first_name="Muhammad", last_name="Ali")
    being_muslim = DietaryRestriction.objects.get(name="22. Muslim")
    assert ali in being_muslim.children.all()
    assert being_muslim in ali.get_all_dietary_restrictions()


@pytest.mark.django_db
def test_muhammad_ali_cannot_eat_pork_chop_sandwiches():
    ali = Child.objects.get(first_name="Muhammad", last_name="Ali")
    pork_chop = Meal.objects.get(name="Pork chop sandwiches")
    assert ali in pork_chop.get_restricted_children()


@pytest.mark.django_db
def test_muslims_cannot_eat_pork_chop_sandwiches():
    being_muslim = DietaryRestriction.objects.get(name="22. Muslim")
    pork_chop = Meal.objects.get(name="Pork chop sandwiches")
    assert pork_chop in being_muslim.meals.all()


@pytest.mark.django_db
def test_joaquin_phoenix_is_vegan():
    joaquin = Child.objects.get(first_name="Joaquin", last_name="Phoenix")
    being_vegan = DietaryRestriction.objects.get(name="21. Vegan")
    assert joaquin in being_vegan.children.all()
    assert being_vegan in joaquin.get_all_dietary_restrictions()


@pytest.mark.django_db
def test_joaquin_phoenix_cannot_eat_pork_chop_sandwiches():
    joaquin = Child.objects.get(first_name="Joaquin", last_name="Phoenix")
    pork_chop = Meal.objects.get(name="Pork chop sandwiches")
    assert joaquin in pork_chop.get_restricted_children()


@pytest.mark.django_db
def test_vegans_cannot_eat_pork_chop_sandwiches():
    being_vegan = DietaryRestriction.objects.get(name="21. Vegan")
    pork_chop = Meal.objects.get(name="Pork chop sandwiches")
    assert pork_chop in being_vegan.meals.all()


@pytest.mark.django_db
def test_carlotta_is_allergic_to_porcini():
    carlotta = Child.objects.get(first_name="Carlotta", last_name="S.")
    porcini_allergy = DietaryRestriction.objects.get(name="Porcini mushrooms")
    assert carlotta in porcini_allergy.children.all()
    assert porcini_allergy in carlotta.get_all_dietary_restrictions()


@pytest.mark.django_db
def test_carlotta_cannot_eat_risotto_ai_porcini():
    carlotta = Child.objects.get(first_name="Carlotta", last_name="S.")
    risotto = Meal.objects.get(name_it="Risotto ai porcini")
    assert carlotta in risotto.get_restricted_children()


@pytest.mark.django_db
def test_people_allergic_to_porcini_cannot_eat_risotto_ai_porcini():
    no_porcini = DietaryRestriction.objects.get(name="Porcini mushrooms")
    risotto = Meal.objects.get(name_it="Risotto ai porcini")
    assert risotto in no_porcini.meals.all()


def test_next_occurrence_datetime_utc_should_be_January_29th():
    rule = rrulestr(
        """
        DTSTART:20250119T120000Z
        RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR
        EXDATE:20250127T120000Z
        """,
    )
    tz = ZoneInfo("UTC")
    next_occurrence = rule.after(datetime(2025, 1, 26, 12, 0, 0, tzinfo=tz))
    assert next_occurrence.date() == date(2025, 1, 29)
    next_occurrence = rule.after(to_aware_datetime(date(2025, 1, 26)))
    assert next_occurrence.date() == date(2025, 1, 29)


def test_next_occurrence_datetime_zh_should_be_January_29th():
    """
    Watch out for the `T11` in the EXDATE corresponding to `T12` in the DTSTART.
    """
    rule = rrulestr(
        """
        DTSTART;TZID=Europe/Zurich:20250119T120000
        RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR
        EXDATE:20250127T110000Z
        """,
    )
    tz = ZoneInfo("Europe/Zurich")
    next_occurrence = rule.after(datetime(2025, 1, 26, 12, 0, 0, tzinfo=tz))
    assert next_occurrence.date() == date(2025, 1, 29)
    next_occurrence = rule.after(to_aware_datetime(date(2025, 1, 26)))
    assert next_occurrence.date() == date(2025, 1, 29)


def test_next_occurrence_date_should_be_January_29th():
    rule = rrulestr(
        """
        DTSTART;VALUE=DATE:20250119
        RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR
        EXDATE;VALUE=DATE:20250127
        """,
    )
    next_occurrence = rule.after(datetime(2025, 1, 26, 12, 0, 0))
    assert next_occurrence.date() == date(2025, 1, 29)
    next_occurrence = rule.after(to_naive_datetime(date(2025, 1, 26)))
    assert next_occurrence.date() == date(2025, 1, 29)


def test_next_occurrence_date_inc_should_be_January_29th():
    rule = rrulestr(
        """
        DTSTART;VALUE=DATE:20250119
        RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR
        EXDATE;VALUE=DATE:20250127
        """,
    )
    next_occurrence = rule.after(datetime(2025, 1, 29, 0, 0, 0), inc=True)
    assert next_occurrence.date() == date(2025, 1, 29)
