def calculate_cost(start_date, return_date, base_price, car_rating):
    """ Takes 2 datetime.date objects base price and a multiplier (rating) and returns total cost (int)

        Mostly for order cost calculation
    """
    nr_of_days = return_date - start_date
    price_per_day = int(base_price * car_rating)
    return nr_of_days.days * price_per_day
