from django.core.exceptions import ValidationError


def validate_menu_categories(value):

    FOOD_CATEGORIES = ["Appetizers", "Main Course", "Desserts"]

    for category in FOOD_CATEGORIES:
        if category not in value:
            raise ValidationError('The menu must include each of the categories "Appetizers", "Main Course", "Desserts".')



