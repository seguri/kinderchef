from modeltranslation.translator import TranslationOptions, register

from .models import DietaryRestriction, Meal


@register(DietaryRestriction)
class DietaryRestrictionTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Meal)
class MealTranslationOptions(TranslationOptions):
    fields = ("name",)
