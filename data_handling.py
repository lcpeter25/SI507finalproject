import csv
import json

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

def convertTreeToDict(location_tree):
    '''Converts a tree formatted as nested lists into a tree formatted as a dictionary so that it can be saved as a JSON.
        Parameters:
            location_tree (list): nested lists with the same country, state, and county information.
        Returns:
            location_dictionary (dict): nested dictionaries with country, state, and county information.
    '''
    location_dictionary = {'United States': {}}
    for state_list in location_tree[1:]:
        location_dictionary['United States'][state_list[0]] = {}
        for county_list in state_list[1:]:
            location_dictionary['United States'][state_list[0]][f'{county_list[0]}'] = []
            for hipov in county_list[1:]:
                location_dictionary['United States'][state_list[0]][f'{county_list[0]}'].append(hipov)
    return location_dictionary


def convertDictToTree(location_dict):
    '''Converts a tree formatted as a dictionary into a tree formatted as nested lists so that it can be used in the program.
        Parameters:
            location_dict (dict): nested dictionaries with country, state, and county information.
        Returns:
            location_list (list): nested lists with the same country, state, and county information.
    '''
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

try:
    location_tree = read_json('location_data.json')
    location_tree = convertDictToTree(location_tree)
except:
    location_tree = ['UNITED STATES', ['ILLINOIS', [('MADISON', 'IL'), [('WASHINGTON', 'MO')], [('JACKSON', 'IL')], [('IRON', 'MO')]], [('COOK', 'IL'), [('LAKE', 'MI')], [('MECOSTA', 'MI')], [('COLES', 'IL')], [('CHAMPAIGN', 'IL')]], [('WAYNE', 'IL'), [('JACKSON', 'IL')], [('ALEXANDER', 'IL')], [('SALINE', 'IL')], [('PULASKI', 'IL')], [('WEBSTER', 'KY')], [('COLES', 'IL')], [('UNION', 'KY')], [('GALLATIN', 'IL')]], [('ROCK ISLAND', 'IL'), [('MCDONOUGH', 'IL')]], [('RANDOLPH', 'IL'), [('JACKSON', 'IL')], [('ALEXANDER', 'IL')], [('IRON', 'MO')], [('SALINE', 'IL')], [('PULASKI', 'IL')], [('WASHINGTON', 'MO')], [('NEW MADRID', 'MO')], [('WAYNE', 'MO')], [('MISSISSIPPI', 'MO')]]], ['INDIANA', [('WELLS', 'IN'), [('DELAWARE', 'IN')]], [('PIKE', 'IN'), [('MONROE', 'IN')], [('GALLATIN', 'IL')], [('GRAYSON', 'KY')], [('WEBSTER', 'KY')], [('COLES', 'IL')], [('UNION', 'KY')]], [('JASPER', 'IN'), [('CHAMPAIGN', 'IL')]], [('GREENE', 'IN'), [('MONROE', 'IN')], [('COLES', 'IL')], [('CHAMPAIGN', 'IL')]], [('LAKE', 'IN'), [('CHAMPAIGN', 'IL')]]], ['MICHIGAN', [('SCHOOLCRAFT', 'MI'), [('LAKE', 'MI')], [('CLARE', 'MI')], [('HOUGHTON', 'MI')]], [('ONTONAGON', 'MI'), [('HOUGHTON', 'MI')]], [('BAY', 'MI'), [('MECOSTA', 'MI')], [('CLARE', 'MI')], [('ISABELLA', 'MI')]], [('OAKLAND', 'MI'), [('WAYNE', 'MI')]], [('OCEANA', 'MI'), [('LAKE', 'MI')], [('MECOSTA', 'MI')]]], ['MINNESOTA', [('ITASCA', 'MN'), [('MAHNOMEN', 'MN')]], [('HENNEPIN', 'MN'), [('THURSTON', 'NE')], [('ROBERTS', 'SD')], [('STORY', 'IA')], [('MAHNOMEN', 'MN')]], [('REDWOOD', 'MN'), [('THURSTON', 'NE')], [('ROBERTS', 'SD')], [('CLAY', 'SD')]], [('ROSEAU', 'MN'), [('MAHNOMEN', 'MN')]], [('RAMSEY', 'MN'), [('STORY', 'IA')], [('MAHNOMEN', 'MN')]]], ['WISCONSIN', [('DANE', 'WI'), [('MENOMINEE', 'WI')]], [('DUNN', 'WI'), [('HOUGHTON', 'MI')], [('STORY', 'IA')], [('MENOMINEE', 'WI')]], [('MILWAUKEE', 'WI'), [('LAKE', 'MI')], [('MENOMINEE', 'WI')]], [('FOREST', 'WI'), [('MENOMINEE', 'WI')]], [('DOUGLAS', 'WI'), [('HOUGHTON', 'MI')], [('MENOMINEE', 'WI')]]]]

location_dictionary = convertTreeToDict(location_tree)
write_json('location_data.json', location_dictionary)
