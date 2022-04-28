from etsy_secrets import ETSY_KEYSTRING, ETSY_SHARED_SECRET
import csv
import json
import requests

ENDPOINT = 'https://openapi.etsy.com/v2/listings/active'

# Utility Functions

def get_api_resource(url, params=None, timeout=10):
    """Returns a response object decoded into a dictionary. If query string < params > are
    provided the response object body is returned in the form on an "envelope" with the data
    payload of one or more SWAPI entities to be found in ['results'] list; otherwise, response
    object body is returned as a single dictionary representation of the SWAPI entity.

    Parameters:
        url (str): a url that specifies the resource.
        params (dict): optional dictionary of querystring arguments.
        timeout (int): timeout value in seconds

    Returns:
        dict: dictionary representation of the decoded JSON.
    """

    if params:
        return requests.get(url, params, timeout=timeout).json()
    else:
        return requests.get(url, timeout=timeout).json()


def read_csv(filepath, encoding='utf-8', newline='', delimiter='\t'):
    """
    Reads a CSV file, parsing row values per the provided delimiter. Returns a list of lists,
    wherein each nested list represents a single row from the input file.

    WARN: If a byte order mark (BOM) is encountered at the beginning of the first line of decoded
    text, call < read_csv > and pass 'utf-8-sig' as the < encoding > argument.

    WARN: If newline='' is not specified, newlines '\n' or '\r\n' embedded inside quoted fields
    may not be interpreted correctly by the csv.reader.

    Parameters:
        filepath (str): The location of the file to read
        encoding (str): name of encoding used to decode the file
        newline (str): specifies replacement value for newline '\n'
                       or '\r\n' (Windows) character sequences
        delimiter (str): delimiter that separates the row values

    Returns:
        list: a list of nested "row" lists
    """

    with open(filepath, 'r', encoding=encoding, newline=newline) as file_obj:
        data = []
        reader = csv.reader(file_obj, delimiter=delimiter)
        for row in reader:
            data.append(row)

        return data


def read_csv_to_dicts(filepath, encoding='utf-8', newline='', delimiter='\t'):
    """Accepts a file path, creates a file object, and returns a list of dictionaries that
    represent the row values using the cvs.DictReader().

    Parameters:
        filepath (str): path to file
        encoding (str): name of encoding used to decode the file
        newline (str): specifies replacement value for newline '\n'
                       or '\r\n' (Windows) character sequences
        delimiter (str): delimiter that separates the row values

    Returns:
        list: nested dictionaries representing the file contents
     """

    with open(filepath, 'r', newline=newline, encoding=encoding) as file_obj:
        data = []
        reader = csv.DictReader(file_obj, delimiter=delimiter)
        for line in reader:
            data.append(line) # OrderedDict()
            # data.append(dict(line)) # convert OrderedDict() to dict

        return data


def read_json(filepath, encoding='utf-8'):
    """Reads a JSON document, decodes the file content, and returns a list or dictionary if
    provided with a valid filepath.

    Parameters:
        filepath (str): path to file
        encoding (str): name of encoding used to decode the file

    Returns:
        dict/list: dict or list representations of the decoded JSON document
    """

    with open(filepath, 'r', encoding=encoding) as file_obj:
        return json.load(file_obj)


def write_json(filepath, data, encoding='utf-8', ensure_ascii=False, indent=2):
    """Serializes object as JSON. Writes content to the provided filepath.

    Parameters:
        filepath (str): the path to the file
        data (dict)/(list): the data to be encoded as JSON and written to the file
        encoding (str): name of encoding used to encode the file
        ensure_ascii (str): if False non-ASCII characters are printed as is; otherwise
                            non-ASCII characters are escaped.
        indent (int): number of "pretty printed" indention spaces applied to encoded JSON

    Returns:
        None
    """

    with open(filepath, 'w', encoding=encoding) as file_obj:
        json.dump(data, file_obj, ensure_ascii=ensure_ascii, indent=indent)


# Globals

zipcodes = read_json(r'c:\Users\peter\Documents\umich\courses\SI507\projects\final_project\final_zipcodes.json')
county_data = read_csv_to_dicts(r'c:\Users\peter\Documents\umich\courses\SI507\projects\final_project\county_data.csv')

clean_county_data = []

for county_datum in county_data:
    if county_datum.get('Hipov'):
        clean_county_data.append(county_datum)

us_state_to_abbrev = {
    "ALABAMA": "AL",
    "ALASKA": "AK",
    "ARIZONA": "AZ",
    "ARKANSAS": "AR",
    "CALIFORNIA": "CA",
    "COLORADO": "CO",
    "CONNECTICUT": "CT",
    "DELAWARE": "DE",
    "FLORIDA": "FL",
    "GEORGIA": "GA",
    "HAWAII": "HI",
    "IDAHO": "ID",
    "ILLINOIS": "IL",
    "INDIANA": "IN",
    "IOWA": "IA",
    "KANSAS": "KS",
    "KENTUCKY": "KY",
    "LOUISIANA": "LA",
    "MAINE": "ME",
    "MARYLAND": "MD",
    "MASSACHUSETTS": "MA",
    "MICHIGAN": "MI",
    "MINNESOTA": "MN",
    "MISSISSIPPI": "MS",
    "MISSOURI": "MO",
    "MONTANA": "MT",
    "NEBRASKA": "NE",
    "NEVADA": "NV",
    "NEW HAMPSHIRE": "NH",
    "NEW JERSEY": "NJ",
    "NEW MEXICO": "NM",
    "NEW YORK": "NY",
    "NORTH CAROLINA": "NC",
    "NORTH DAKOTA": "ND",
    "OHIO": "OH",
    "OKLAHOMA": "OK",
    "OREGON": "OR",
    "PENNSYLVANIA": "PA",
    "RHODE ISLAND": "RI",
    "SOUTH CAROLINA": "SC",
    "SOUTH DAKOTA": "SD",
    "TENNESSEE": "TN",
    "TEXAS": "TX",
    "UTAH": "UT",
    "VERMONT": "VT",
    "VIRGINIA": "VA",
    "WASHINGTON": "WA",
    "WEST VIRGINIA": "WV",
    "WISCONSIN": "WI",
    "WYOMING": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "PUERTO RICO": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}

no_inputs = ['n', 'no', 'false', 'incorrect', 'wrong', 'nope']
yes_inputs = ['y', 'yes', 'yeah', 'correct', 'right', 'yep']
accepted_inputs = no_inputs + yes_inputs


# Location-Based Functions

def getLatLong(zipcode):
    '''This function converts a zipcode into a latitude and longitude.
            Parameters:
                zipcode (str): a 5-digit US zipcode, except it may be fewer digits because leading zeroes are removed.

            Returns:
                user_lat_long (tuple): a (latitude, longitude) tuple that contains strings (that are float-convertible).'''

    for zip in zipcodes:
            if zip['zip'] == zipcode:
                user_lat_long = (zip['Latitude'], zip['Longitude'])
    return user_lat_long


def getCloseZipcodes(lat_long, distance=1):
    '''This function provides a list of zipcodes (in dict objects that provide additional data as well) that are within +-1 (or another, larger
        distance can be added if necessary) degree lat and long from the original location.
        Parameters:
            lat_long (tuple): a tuple of strings that represent lat and long coornidates.
            distance (int): default 1, used to expand the search area if there are no High Poverty counties within +-1 degree lat and long.
        Returns:
            close_zipcodes (list): a list of dictionaries that have zipcode and other information for locations near the original location.
    '''

    lat, long = lat_long
    lat = float(lat)
    long = float(long)
    close_zipcodes = []
    for zip in zipcodes:

        if (lat - distance) < float(zip.get('Latitude')) < (lat + distance) and (long - distance) < float(zip.get('Longitude')) < (long + distance):
            close_zipcodes.append(zip)

    return close_zipcodes


def getCounties(zips):
    '''This function takes a list of zipcodes (in dict objects that provide additional data as well)
        and tells you which counties are represented in that list.
        Parameters:
            zips (list): a list of dictionaries that give information about a zipcode
        Returns:
            counties (list): a list of tuples that show ('County', 'State Postal Code') '''

    counties = []

    for zip in zips:

        if not (zip.get('County Name'), zip.get('State')) in counties:
            counties.append((zip.get('County Name'), zip.get('State')))

    return counties


def getNearbyCounties(zipcode, distance=1):
    '''This function provides the counties that are near a given zipcode.
        Parameters:
            zipcode (str): a 5-digit US zipcode, except it may be fewer digits because leading zeroes are removed.
            distance (int): default 1, used to expand the search area if there are no High Poverty counties within +-1 degree lat and long.
        Returns:
            counties (list): a list of tuples that show ('County', 'State Postal Code')'''

    lat_long = getLatLong(zipcode)

    close_zips = getCloseZipcodes(lat_long, distance)

    return getCounties(close_zips)


def keepHighPoverty(counties):
    '''This function takes a list of counties and returns a list with only the high-poverty counties.
        Parameters:
            counties (list): a list of tuples that show ('County', 'State Postal Code')
        Returns:
            high_poverty_counties (list): a list of tuples that show ('County', 'State Postal Code')
    '''

    high_poverty_counties = []
    for county in counties:
        county, state = county
        for county_datum in clean_county_data:
            if county.lower() == county_datum.get('County').lower() and state.lower() == county_datum.get('State').lower():

                if county_datum.get('Hipov') == '1':
                    high_poverty_counties.append((county, state))

    return high_poverty_counties


def findAllZipsInCounty(county, state):
    '''This function creates a list of all of the zipcodes in a specific county.
        Parameters:
            county (str): name of a county
            state (str): two-letter postal code of a US state
        Returns:
            zips (list): a list of all the zipcodes in that county
    '''

    zips = []
    for zipcode in zipcodes:

        if county.lower() == zipcode.get('County Name').lower() and state.lower() == zipcode.get('State').lower():
            zips.append(zipcode.get('zip'))

    return zips


def findAllLocationsInCounty(county, state):
    '''This function creates a list of all of the 'Zipcode names' ('City, ST') in a specific county.
        Parameters:
            county (str): name of a county
            state (str): two-letter postal code of a US state
        Returns:
            zips (list): a list of all the zipcode names in that county, no duplicates
    '''
    locations = []
    for zipcode in zipcodes:

        if county.lower() == zipcode.get('County Name').lower() and state.lower() == zipcode.get('State').lower():
            locations.append(zipcode.get('Zipcode name'))

    return list(set(locations))


def getNearbyHipovCountiesByCounty(county_and_state):
    '''This function will give a list of high poverty counties near a given county.
        Parameters:
            county_and_state (tuple): a tuple of strings (county, state_postal_code)
        Returns:
            high_poverty_counties (list): a list of tuples that show ('County', 'State Postal Code')
    '''
    county, state = county_and_state

    distance = 1
    while True:
        zips = findAllZipsInCounty(county, state)
        hipov_counties = []
        for zip in zips:

            nearby_counties = getNearbyCounties(zip, distance)
            hipov_counties += keepHighPoverty(nearby_counties)

        if hipov_counties:
            break
        else:
            distance += 1
    return list(set(hipov_counties))


# Play-Based Functions

def addHipovCountyLeaves(county_and_state_list):
    '''This function takes a list (a branch of a tree) and adds leaves to the list. The 0 index item of the list is the user's location and the rest of the 
        items (the leaves) are the nearby high-poverty counties. 
        Parameters:
            county_and_state_list (list): a list of one tuple ('County', 'ST') that represents the county location of the user. This is the base of the branch.
        Returns: 
            county_and_state_list (list): a list of tuples ('County', 'ST'). The 0 index item of the list is the user's location and the rest of the 
        items (the leaves) are the nearby high-poverty counties.
    '''
    hipov_counties = getNearbyHipovCountiesByCounty(county_and_state_list[0])
    for hipov_county in hipov_counties:
        county_and_state_list.append([hipov_county])

    return county_and_state_list


def checkState(state):
    '''Checks to make sure that a user input is a valid state name, reprompts until a correct state name is entered and returned.
        Parameters:
            state (str): a user-produced string that should be the name of a state.
        Returns:
            state (str): a valid state name.
    '''

    if state.upper() in us_state_to_abbrev.keys():
        return state.upper()
    else:
        print('State name not valid.')
        state = checkState(input('Enter a valid state name: '))
        return state.upper()

def addState(tree, state):
    '''Adds a new state into a location tree (nested lists).
        Parameters:
            tree (list): nested lists that represent a tree of Country - States - Counties.
            state (str): the full name of a state, will be checked for validity.
        Returns:
            tree (list): nested lists that represent a tree of Country - States - Counties. Now with an added state at the end of the list,
                        formatted so that counties may be added.
    '''

    new_branch = [state.upper()]
    tree.append(new_branch)
    return tree


def checkCounty(county, state):
    '''Checks to make sure that a user input is a valid county name, reprompts until a correct county name is entered and returned.
        Parameters:
            county (str): a user-produced string that should be the name of a county.
            state (str): string name of a US state.
        Returns:
            county (str): a valid county name.
    '''
    state_abbrev = us_state_to_abbrev.get(state)

    valid = False
    for zipcode in zipcodes:
        if county.lower() == zipcode.get('County Name').lower() and state_abbrev.lower() == zipcode.get('State').lower():
            valid = True

    if valid:
        return county.upper()
    else:
        print('County not found in selected state.')
        county = checkCounty(input('Enter a valid county name: '), state)
        return county.upper()

def addCounty(tree, county):
    '''Adds a new county into a location tree (nested lists).
        Parameters:
            tree (list): nested lists and tuples that represent a tree of State - Counties.
            county (str): the name of a county, will be checked for validity.
        Returns:
            tree (list): nested lists and tuples that represent a tree of State - Counties. Now with the added county at the end, along with its
                            nearby high-poverty counties.
    '''
    state = tree[0]
    state_abbrev = us_state_to_abbrev.get(state)

    new_branch = [(county.upper(), state_abbrev)]

    new_branch = addHipovCountyLeaves(new_branch)

    tree.append(new_branch)
    return tree


def convertTreeToDict(location_tree):
    location_dictionary = {'United States': {}}
    for state_list in location_tree[1:]:
        location_dictionary['United States'][state_list[0]] = {}
        for county_list in state_list[1:]:
            location_dictionary['United States'][state_list[0]][f'{county_list[0]}'] = []
            for hipov in county_list[1:]:
                location_dictionary['United States'][state_list[0]][f'{county_list[0]}'].append(hipov)
    return location_dictionary


def convertDictToTree(location_dict):
    location_list = ['United States']
    for state_key in location_dict['United States'].keys():
        state_list = [state_key]
        location_list.append(state_list)
        for county_key in location_dict['United States'][state_key].keys():
            new_county_key = [(county_key[2:-8], county_key[-4:-2])]
            state_list.append(new_county_key)
            for hipov in location_dict['United States'][state_key][county_key]:
                new_county_key.append(hipov)
    return location_list


def yes(prompt):
    """
    This function determines if the user thinks the question is true or false, it handles invalid answers by reprompting.
        Parameter(s):
            prompt: a string response to an input("Question?")

        Return:
            True if the response is some version of "yes."
            False if the response is some version of "no."
    """

    if prompt.lower() in yes_inputs:
        return True
    elif prompt.lower() in no_inputs:
        return False
    else:
        print('That answer is not understood; please use one of the following:')
        for accepted_input in accepted_inputs:
            print(accepted_input)
        if yes(input('Valid input: ')):
            return True
        else:
            return False

def printChildren(tree):
    '''Given a tree (list), this function will print all of the children in that branch.
        Parameters:
            tree (list): nested list of lists that represents a tree.
        Returns:
            children (list): a list that contains only the direct children of the root node of the original tree.
    '''
    children = []
    for child in tree[1:]:
        children.append(child[0])
    print(children)
    return children

def isNumber(number):
    '''Checks to make sure that a user input is a valid int, reprompts until a correct integer number is entered and returned.
        Parameters:
            number (str): a user-produced string that should be convertible to int.
        Returns:
            number (int): an integer
    '''
    try:
        number = int(number)
        return number
    except:
        number = input('Please enter a valid integer (e.g. 1, 3, 10): ')
        number = isNumber(number)
        return number


# Etsy Functions

def getListings(location, tag=None):
    '''Gets Etsy listings for shops based in the given location. Optional tag will further filter results.
        Parameters:
            location (str): a "City, ST" string representing a location.
            tag (str): default None, a string that can filter the type of object in the Etsy listing, such as "necklace"
        Returns:
            listings (list): a list of dictionaries that each represent an Etsy listing
    '''
    if tag:
        listings = get_api_resource(ENDPOINT, {'api_key': ETSY_KEYSTRING, 'location': location, 'tags': tag})
    else:
        listings = get_api_resource(ENDPOINT, {'api_key': ETSY_KEYSTRING, 'location': location})

    return listings['results']

def allListingsInCounties(counties, tag=None):
    '''Given a list of counties, this function will find all the Etsy listings from shops based in those counties.
        The optional tag parameter can further filter results.
            Parameters:
                counties (list): a list of tuples that represent counties ('County', 'ST').
                tag (str): default None, a string that can filter the type of object in the Etsy listing, such as "necklace"
            Returns:
                listings (list): list of dictionaries that each represent an Etsy listing
    '''
    listings = []

    for county in counties:
        county, state = county
        locations = findAllLocationsInCounty(county, state)

        for location in locations:
            new_listings = getListings(location, tag=tag)

            for new_listing in new_listings:
                listings.append(new_listing)

    return listings

def printListings(listings):
    '''Prints Etsy listings for consumption by the user. Outputs the title and url for each listing.
        Parameters:
            listings (list): list of dictionaries that each represent an Etsy listing
        Returns:
            None
    '''
    for listing in listings:
        title = listing['title']
        url = listing['url']
        print(f'{title}: {url}\n')


############################################################################################################


def main():

    try:
        location_tree = read_json('location_data.json')
        location_tree = convertDictToTree(location_tree)
    except:
        location_tree = ['UNITED STATES', ['ILLINOIS', [('MADISON', 'IL'), [('WASHINGTON', 'MO')], [('JACKSON', 'IL')], [('IRON', 'MO')]], [('COOK', 'IL'), [('LAKE', 'MI')], [('MECOSTA', 'MI')], [('COLES', 'IL')], [('CHAMPAIGN', 'IL')]], [('WAYNE', 'IL'), [('JACKSON', 'IL')], [('ALEXANDER', 'IL')], [('SALINE', 'IL')], [('PULASKI', 'IL')], [('WEBSTER', 'KY')], [('COLES', 'IL')], [('UNION', 'KY')], [('GALLATIN', 'IL')]], [('ROCK ISLAND', 'IL'), [('MCDONOUGH', 'IL')]], [('RANDOLPH', 'IL'), [('JACKSON', 'IL')], [('ALEXANDER', 'IL')], [('IRON', 'MO')], [('SALINE', 'IL')], [('PULASKI', 'IL')], [('WASHINGTON', 'MO')], [('NEW MADRID', 'MO')], [('WAYNE', 'MO')], [('MISSISSIPPI', 'MO')]]], ['INDIANA', [('WELLS', 'IN'), [('DELAWARE', 'IN')]], [('PIKE', 'IN'), [('MONROE', 'IN')], [('GALLATIN', 'IL')], [('GRAYSON', 'KY')], [('WEBSTER', 'KY')], [('COLES', 'IL')], [('UNION', 'KY')]], [('JASPER', 'IN'), [('CHAMPAIGN', 'IL')]], [('GREENE', 'IN'), [('MONROE', 'IN')], [('COLES', 'IL')], [('CHAMPAIGN', 'IL')]], [('LAKE', 'IN'), [('CHAMPAIGN', 'IL')]]], ['MICHIGAN', [('SCHOOLCRAFT', 'MI'), [('LAKE', 'MI')], [('CLARE', 'MI')], [('HOUGHTON', 'MI')]], [('ONTONAGON', 'MI'), [('HOUGHTON', 'MI')]], [('BAY', 'MI'), [('MECOSTA', 'MI')], [('CLARE', 'MI')], [('ISABELLA', 'MI')]], [('OAKLAND', 'MI'), [('WAYNE', 'MI')]], [('OCEANA', 'MI'), [('LAKE', 'MI')], [('MECOSTA', 'MI')]]], ['MINNESOTA', [('ITASCA', 'MN'), [('MAHNOMEN', 'MN')]], [('HENNEPIN', 'MN'), [('THURSTON', 'NE')], [('ROBERTS', 'SD')], [('STORY', 'IA')], [('MAHNOMEN', 'MN')]], [('REDWOOD', 'MN'), [('THURSTON', 'NE')], [('ROBERTS', 'SD')], [('CLAY', 'SD')]], [('ROSEAU', 'MN'), [('MAHNOMEN', 'MN')]], [('RAMSEY', 'MN'), [('STORY', 'IA')], [('MAHNOMEN', 'MN')]]], ['WISCONSIN', [('DANE', 'WI'), [('MENOMINEE', 'WI')]], [('DUNN', 'WI'), [('HOUGHTON', 'MI')], [('STORY', 'IA')], [('MENOMINEE', 'WI')]], [('MILWAUKEE', 'WI'), [('LAKE', 'MI')], [('MENOMINEE', 'WI')]], [('FOREST', 'WI'), [('MENOMINEE', 'WI')]], [('DOUGLAS', 'WI'), [('HOUGHTON', 'MI')], [('MENOMINEE', 'WI')]]]]


    print("Welcome to Gifts for Good! This app suggests items for purchase that are sold by Etsy stores")
    print("in areas near you that are experiencing high poverty. We encourage shoppers to keep money in their")
    print("local communities, where it is needed most.")
    us_answer = input("\nFirst, let's determine your location. Are you located in the United States? ")

    while not yes(us_answer):
        print('\nSorry, but we only support US locations at this time.')
        answer = input('Would you like to search for items near a US location? ')
        if yes(answer):
            break
        else:
            print("Goodbye!")
            quit()

    print('\n')
    print('Currently mapped states:')
    states = printChildren(location_tree)
    print('\n')
    state = input("Please enter the name of your state. We will add it to our mapping if it is not yet listed.\n").upper()

    state = checkState(state)

    if state not in states:
        location_tree = addState(location_tree, state)
        states.append(state)

    index = states.index(state)
    state_tree = location_tree[index+1]

    print('\n')
    print(f"Currently mapped counties in {state}:")
    counties = printChildren(state_tree)
    print('\n')
    county = input(
                    '''Please enter the name of your county. We will add it to our mapping if it is not yet listed.\n
                    Only county name is required. Do not include state information.\n''').upper()

    county = checkCounty(county, state)

    county_tuple = (county, us_state_to_abbrev.get(state))

    if county_tuple not in counties:
        state_tree = addCounty(state_tree, county)
        counties.append(county_tuple)

    index = counties.index(county_tuple)
    county_tree = state_tree[index+1]

    location_dictionary = convertTreeToDict(location_tree)
    write_json('location_data.json', location_dictionary)

    print('\n')
    print(f'The following counties near {county} county, {state}, experience high poverty levels.')
    hipov_counties = printChildren(county_tree)

    print('\n')
    answer = input('''Would you like to limit your Etsy item search to one specific high-poverty county? ''')
    if yes(answer):
        # reassign hipov_counties to be a list with only the selected county
        county = input(
                    '''Please enter the name of the county you'd like to search. Only county name is required. Do not include state information.\n''').upper()

        county = checkCounty(county, state)

        county_tuple = (county, us_state_to_abbrev.get(state))

        if county_tuple in hipov_counties:
            hipov_counties = [county_tuple]
            print(f'\nThanks! We will only search in {county} county.')
        else:
            print('County not recognized. Searching all counties...')

    print('\n')
    tag_answer = input('''Would you like to add a tag to narrow your search (e.g. 'necklace' or 'watch')? ''')

    print('\n')
    if yes(tag_answer):
        tag = input('Please enter your desired tag now: ')
        print('\n')
        print(f'Searching for {tag}...')
        print('\n')
    else:
        tag = None

    print('This next step may take a while. Please be patient as we gather Etsy listings...')
    print('\n')

    listings = allListingsInCounties(hipov_counties, tag)
    printListings(listings[:100])

    print('\n')
    while True:
        answer = input('Would you like to see more results? ')
        start = 100
        if yes(answer):
            add_listings = input('How many more listings would you like to see? ')
            add_listings = isNumber(add_listings)
            end = start + add_listings
            printListings(listings[start:end])
            start = end
        else:
            break

    print('\n')
    print('Thank you for using Gifts for Good! Remember to shop small and support your neighbors!')

    print('\n')
    print('(Added state and county data have been saved for future use, if applicable. Thank you for expanding our mapping!)')




if __name__ == '__main__':
    main()