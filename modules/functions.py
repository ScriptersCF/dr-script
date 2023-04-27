import sqlite3
import re
from modules import data

# handle_data: sets and gets data from the database
def handle_data(command, args):
    # open database & execute passed command
    database = sqlite3.connect("scores.sqlite")
    cursor = database.cursor()
    cursor.execute(command, args)
    
    # fetch all returned data, commit changes and close database
    data = cursor.fetchall()
    database.commit()
    database.close()

    # if data is in extraneous list, remove the list & return data
    if data:
        if len(data) == 1 and isinstance(data, list):
            return data[0]
    
    # otherwise, just return data as is
    return data


# get_data: gets data from the database, or creates a new entry if none exists
def get_data(user_id):
    # if data doesn't exist, give user default amount of points
    user_data = handle_data("SELECT * FROM scores WHERE userId = (?)", (user_id,))

    # if user exists in database, return data
    if user_data:
        return user_data

    # otherwise, add user to database
    handle_data("INSERT INTO scores (userId, points, level) VALUES ((?), (?), (?))",
        (str(user_id), 1, 1))

    # return new data
    return handle_data("SELECT * FROM scores WHERE userId = (?)", (user_id,))


# has_custom_colour: checks if user has a custom colour, returns it if so
async def has_custom_colour(user):
    # for each user role, return truthy value if it's a custom colour
    for role in user.roles:
        if role.name in data.colour_list:
            return role
    
    # otherwise, return false
    return False


# verify_sell_hire_name: checks if a forum post on sell and hire follows the naming conventions listed in rules
async def verify_sell_hire_name(name : str):
    # post names must start with a price listed in square brackets
    has_price_in_brackets = re.match("^[(.*?)]", name)

    return has_price_in_brackets
