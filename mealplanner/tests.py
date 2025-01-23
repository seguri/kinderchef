import pytest

from mealplanner.models import Child, DietaryRestriction, Meal


@pytest.mark.django_db
def test_muhammad_ali_is_muslim():
    ali = Child.objects.get(first_name="Muhammad", last_name="Ali")
    being_muslim = DietaryRestriction.objects.get(name="22. Muslim")
    assert ali in being_muslim.children.all()


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
