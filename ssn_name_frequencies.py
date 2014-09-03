from datetime.date import today

from requests import post


def check_parameters(year, name_gender_is_male, count_returned):
    '''
    Check whether the passed parameters are valid, returning errors if
    inappropriate values exist
    '''

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

def get_response_from_ssa(year, percentage_instead_of_frequency):
    '''
    Retrieve the HTML response from the Social Security website, which
    will include the table with name frequencies, or any errors
    '''

    SSA_URL = "http://www.ssa.gov/cgi-bin/popularnames.cgi"
    HIGHEST_NAME_COUNT_ALLOWED = 1000

    # Gather the information from the SSA website
    if percentage_instead_of_frequency:
        number_parameter = "p"
    else:
        number_parameter = "n"

    parameters = {
            "year": year,
            "top": HIGHEST_NAME_COUNT_ALLOWED,
            "number": number_parameter
            }
    response = post(SSA_URL, params=parameters)

    # Make sure that the response was successful
    if response.status_code is not 200:
        response.raise_for_status()

    # Return the responded HTML text
    return response.text

def parse_table(returned_text):
    '''Extract the table data from the provided HTML'''
    
    pass


def main(year, name_gender_is_male, count_returned=1000):
    '''
    The main function of this package, which returns a list of the top
    names of a given gender for a given year, and their frequencies
    and relative frequencies (ie, percentages)
    '''

    # Check user-provided parameters, throwing an error if they are invalid
    check_parameters(
            year=year,
            name_gender_is_male=name_gender_is_male,
            count_returned=count_returned
            )

    # Get the data from the SSA website
    frequencies = parse_table(get_response_from_ssa(
            year=year,
            percentage_instead_of_frequency=False
            ))
    percentages = parse_table(get_response_from_ssa(
            year=year,
            percentage_instead_of_frequency=False
            ))

    # Keep only the desired gender of names

    # Merge the frequencies and the percentages together

    # Subset to the desired number of names
    names = names[0:(count_returned - 1)]

    # Return the parsed and subset data
    return names
