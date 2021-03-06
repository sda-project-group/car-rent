#self created file to store custom validators

from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from datetime import date


def validation_age(birthdate):
    adult_age = 18
    date_today = date.today()
    year = date_today.year
    min_birthday = date_today.replace(year=year - adult_age)
    if min_birthday < birthdate < date_today:
        raise ValidationError("Niestety nie jesteś pełnoletni/nia i nie możesz skorzystać z naszych usług")
    elif birthdate > date_today:
        raise ValidationError("Nieprawidłowa data urodzenia")

