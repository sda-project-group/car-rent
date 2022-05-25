from django.core.exceptions import ValidationError
from datetime import date
from carrentapp.models import Order


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
def if_entries_collide_error(start_date, return_date, car):
    colliding_entries = Order.objects.filter(
                            status='Aktywny',
                            car=car,
                            start_date__range=(start_date, return_date)) | \
                        Order.objects.filter(
                            status='Aktywny',
                            car=car,
                            return_date__range=(start_date, return_date))
    if colliding_entries:
        raise ValidationError("Ten samochód jest niedostępny w tych terminach")


