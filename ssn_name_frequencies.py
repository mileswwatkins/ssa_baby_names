from datetime.date import today

from requests import post


def parse_table(returned_table):
    ''''''
    pass

def is_year_valid(returned_html):
    ''''''
    return True

def get_response_from_ssa(year, name_gender_is_male, count_returned=1000):
    ''''''

    # Check parameters
    check_parameters(
            year=year,
            name_gender_is_male=name_gender_is_male,
            count_returned=count_returned
            )

    parameters = 
    response = post()

def check_parameters(year, name_gender_is_male, count_returned):
    '''Check whether the passed parameters are valid'''

    # Check year, which must be between 1880 and last year
    LOWEST_YEAR_ALLOWED = 1880
    highest_year_allowed = today().year - 1
    if not LOWEST_YEAR_ALLOWED <= year <= highest_year_allowed:
        raise ValueError("Data do not exist for the given year")
    if type(year) is not int:
        raise TypeError("year parameter must be an integer")

    # Check that name_gender_is_male is a boolean
    if type(name_gender_is_male) is not bool:
        raise TypeError("name_gender_is_male must be True (returns male names) or False (female names)")

    # Check that count_returned is an integer between 1 and 1000
    LOWEST_COUNT_ALLOWED = 1
    HIGHEST_COUNT_ALLOWED = 1000
    if type(count_returned) is not int or \
            count_returned < LOWEST_COUNT_ALLOWED or \
            count_returned > HIGHEST_COUNT_ALLOWED:
        raise ValueError("count_returned must be a positive integer between {0} and {1}".format(
                (LOWEST_COUNT_ALLOWED, HIGHEST_COUNT_ALLOWED)))