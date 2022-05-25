from datetime import date

from django.core.exceptions import ValidationError

from carrentapp.models import Order


def catch_validation_error(func):
    """Takes a validator function, catches ValidationError and returns its message string"""
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except ValidationError as error:
            return error.message

    return wrapper


@catch_validation_error
def order_date_validator(start_date, return_date, option=None, option_value=None):
    """
    takes in 2 datetime.date objects and raises Validation error if below conditions are true

    also takes an optional argument option in str format: possible options: 'only_longer'
    """

    if start_date < date.today() and option is None:
        print(option)
        raise ValidationError("Data wypożyczenia nie może być w przeszłości!")

    if return_date <= start_date:
        raise ValidationError("Data zwrotu musi byc co najmniej o dzien wieksza od daty wypożyczenia!")

    if option is not None and return_date < option_value:
        raise ValidationError("Skracanie rozpoczętych zamówień nie jest dozowlone")


@catch_validation_error
def if_entries_collide_error(start_date, return_date, car, order_id=None):

    if order_id is not None:
        colliding_entries = Order.objects.exclude(id=order_id)
        colliding_entries = colliding_entries.filter(
                                status='Aktywny',
                                car=car,
                                start_date__range=(start_date, return_date)) | \
                            colliding_entries.filter(
                                status='Aktywny',
                                car=car,
                                return_date__range=(start_date, return_date))

        if colliding_entries:
            raise ValidationError("Ten samochód jest niedostępny w tych terminach.")
    else:
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
