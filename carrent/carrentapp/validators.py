#self created file to store custom validators

from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from datetime import date


def catch_validation_error(func):
    """Takes a validator function, catches ValidationError and returns its message string"""
    def wrapper(*args):
        try:
            func(*args)
        except ValidationError as error:
            return error.message

    return wrapper


@catch_validation_error
def order_date_validator(start_date, return_date):
    """ takes in 2 datetime.date objects and raises Validation error if below conditions are true"""

    if start_date < date.today():
        raise ValidationError("Data wypożyczenia nie może być w przeszłości!")

    if return_date <= start_date:
        raise ValidationError("Data zwrotu musi byc co najmniej o dzien wieksza od daty wypożyczenia!")


@catch_validation_error
def if_found_in_db(query_set):
    if query_set:
        raise ValidationError("Ten samochód jest niedostępny w tych terminach")

