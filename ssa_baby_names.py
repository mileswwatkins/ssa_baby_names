import datetime
import re
from xml.etree import cElementTree as ET

import requests
        

# Set package constants
HIGHEST_NAME_COUNT_ALLOWED = 1000


def check_parameters(year, name_gender_is_male):
    '''
    Check whether the passed parameters are valid, returning errors if
    inappropriate values exist
    '''

    # Check year, which must be between 1880 and last year
    LOWEST_YEAR_ALLOWED = 1880
    highest_year_allowed = datetime.date.today().year - 1
    if not LOWEST_YEAR_ALLOWED <= year <= highest_year_allowed:
        raise ValueError("Data do not exist for the given year")
    if type(year) is not int:
        raise TypeError("year parameter must be an integer")

    # Check that name_gender_is_male is a boolean
    if type(name_gender_is_male) is not bool:
        raise TypeError("name_gender_is_male must be True (returns male names) or False (female)")


def get_response_from_ssa(year, percentage_instead_of_frequency):
    '''
    Retrieve the HTML response from the Social Security website, which
    will include the table with name frequencies, or any errors
    '''

    SSA_URL = "http://www.ssa.gov/cgi-bin/popularnames.cgi"

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
    response = requests.post(SSA_URL, data=parameters)

    # Make sure that the response was successful
    if response.status_code is not 200:
        response.raise_for_status()

    # Return the responded HTML text
    return response.text


def parse_table(returned_html):
    '''
    Extract the table data from the provided HTML.

    According to the HTML <meta> information, the response's structure
    has been consistent since 2006, so this function should not need
    regular changes.
    '''
    
    # Extract the names table from the full HTML page
    # There are multiple <table>s,
    # use the one with <... summary="Popularity for top [number]...">
    NAME_TABLE_SEARCH = r'''
            Background\ information.*? # Use the first table after the title
            (
            <table.*?</table> # Find the main body of the table
            </p>\s</td></tr></table> # Also capture the hanging tags to fix
            )
            '''
    table_html_needing_fix = re.findall(
            NAME_TABLE_SEARCH,
            returned_html,
            re.DOTALL | re.VERBOSE
            )[0]

    # The table also has improper HTML tagging in the footer, requiring fixes
    NAME_TABLE_FIX = r'''(<tr.*)<tr><td colspan="'''
    table_html = "<table>" + \
            re.findall(
            NAME_TABLE_FIX,
            table_html_needing_fix,
            re.DOTALL
            )[0] + \
            "</table>"

    # Parse the table into memory
    table_parser = ET.XML(table_html)
    rows = iter(table_parser)

    # Confirm that the column names are as expected
    EXPECTED_COLUMN_NAMES_FREQUENCY = [
            "Rank",
            "Male name",
            "Number of",
            "Female name",
            "Number of"
            ]
    EXPECTED_COLUMN_NAMES_PERCENTAGE = [
            "Rank",
            "Male name",
            "Percent of",
            "Female name",
            "Percent of"
            ]
    column_names = [header.text for header in next(rows)]
    if column_names == EXPECTED_COLUMN_NAMES_FREQUENCY:
        table_type = "frequency"
    elif column_names == EXPECTED_COLUMN_NAMES_PERCENTAGE:
        table_type = "percentage"
    else:
        raise SyntaxError("The SSA's HTML response has changed, please try to update this package")

    # Finish parsing the table rows
    male_table = []
    female_table = []
    for row in rows:
        cell_values = [value.text for value in row]

        # Destring the value fields
        if table_type == "frequency":
            male_value = int(cell_values[2].replace(",", ""))
            female_value = int(cell_values[4].replace(",", ""))
        elif table_type == "percentage":
            male_value = float(cell_values[2].replace("%", ""))
            female_value = float(cell_values[4].replace("%", ""))

        # Restructure the columns so that male and female data are separated
        male_data = {
                "name": cell_values[1],
                "value": male_value
                }
        male_table.append(male_data)

        female_data = {
                "name": cell_values[3],
                "value": female_value
                }
        female_table.append(female_data)

    table = {"male": male_table, "female": female_table}
    return table


class YearOfBabyNames(list):
    '''Container for all <BabyName>s in a given year'''

    def __init__(self, year, name_gender_is_male):
        self.year = year
        self.name_gender_is_male = name_gender_is_male

    def __repr__(self):
        if self.name_gender_is_male:
            gender = "males"
        else:
            gender = "females"

        return "<YearOfBabyNames for {0} in the year {1}>".format(
                gender, self.year
                )

    def lookup(self, name_to_lookup):
        '''Find a given <BabyName> within the year, by name'''
        for baby_name in self:
            if baby_name.name.lower() == name_to_lookup.lower():
                return baby_name

        # If the given name isn't found, then this error will be thrown
        raise KeyError(""""{0}" is not in the top {1} names for the year {2}""".format(
                name_to_lookup, HIGHEST_NAME_COUNT_ALLOWED, self.year
                ))

    def top(self):
        '''Return the most popular <BabyName> for the year'''
        for baby_name in self:
            if baby_name.rank == 1:
                return baby_name


class BabyName(object):
    '''Information about a particular given name in a particular year'''

    def __init__(self, name, rank, frequency, percentage):
        self.name = name
        self.rank = rank
        self.frequency = frequency
        self.percentage = percentage

    def __repr__(self):
        return """<BabyName for "{}">""".format(self.name)


def get_top_names(year, name_gender_is_male):
    '''
    The main function of this package, which returns a list of the top
    names of a given gender for a given year, and their frequencies
    and relative frequencies (ie, percentages of all births)
    '''

    # Check user-provided parameters, throwing an error if they are invalid
    check_parameters(
            year=year,
            name_gender_is_male=name_gender_is_male
            )

    # Get the data from the SSA website
    frequencies = parse_table(get_response_from_ssa(
            year=year,
            percentage_instead_of_frequency=False
            ))
    percentages = parse_table(get_response_from_ssa(
            year=year,
            percentage_instead_of_frequency=True
            ))

    # Keep only the desired gender of names
    if name_gender_is_male:
        frequencies = frequencies["male"]
        percentages = percentages["male"]
    else:
        frequencies = frequencies["female"]
        percentages = percentages["female"]

    # Merge the frequencies and the percentages together
    names = YearOfBabyNames(
            year=year,
            name_gender_is_male=name_gender_is_male
            )
    for name_index in range(HIGHEST_NAME_COUNT_ALLOWED):

        # Make sure that both tables have the names in the same order
        if frequencies[name_index]["name"] != percentages[name_index]["name"]:
            AssertionError("The baby names are in a different order in the two SSA tables")

        name = BabyName(
                name=frequencies[name_index]["name"],
                rank=name_index + 1,
                frequency=frequencies[name_index]["value"],
                percentage=percentages[name_index]["value"]
                )

        names.append(name)

    # Return the parsed and subset data, in neat object form
    return names
