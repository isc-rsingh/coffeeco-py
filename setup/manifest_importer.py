import os
import json
import iris
from datetime import date

# status = iris.User.EmbeddedPython.Test()
SETUPDIR = "/irisdev/app/setup"
KEYFIELDNAMES = ["vendor_id", "vendor_product_code", "quantity_kg"]

def load_manifest(json_data: dict):
    """ Use SQL INSERT statements to load records into existing relational tables
    Args:
        json_data: manifest in a Python dictionary
        conn: database connection object
    Returns:
        None if creation is successful, otherwise returns the exception
    """
    today = date.today()
    mydate = today.strftime("%Y-%m-%d")
    fieldnamesql = "INSERT INTO ICO.inventory (vendor_id, vendor_product_code, quantity_kg, date_arrival)"
    try:
        items = json_data.get("items")
        if items is None:
            raise Exception("No items to load in manifest.")
        for item in items:
            valsql = fieldnamesql + " VALUES ("
            valsql += "'" + item.get("vendor_id") + "', "
            valsql += "'" + item.get("vendor_product_code") + "', "
            valsql += str(item.get("quantity_kg")) + ", "
            valsql += "TO_DATE('" + mydate + "', 'YYYY-MM-DD') )"
            print("Inserting: "+valsql)
            sql = iris.sql.prepare(valsql)
            sql.execute()
            # cursor.execute(valsql)
    except Exception as exp:
        return exp

    return None


def validate_manifest(json_data: dict) -> tuple:
    """ Verify that the manifest file contains valid inventory data
    Args:
        json_data: manifest in a Python dictionary
    Returns:
        a tuple (original JSON data, True, None) if valid, (None, false, exception) if not
    """
    try:
        # check if items exists
        if (json_data.get("items")) is None:
            raise Exception("No items key in JSON")
        # check if items is an array
        items = json_data.get("items")
        if (not isinstance(items, list)):
            raise Exception("items is not an array.")
        # check if all fields exist
        for item in items:
            num_good_keys = 0
            for key in item:
                if (key in KEYFIELDNAMES):
                    num_good_keys += 1
            if num_good_keys < len(KEYFIELDNAMES):
                raise Exception("Bad data in items.")
        return json_data, True, None
    except Exception as exp:
        return None, False, exp

def get_connection_info(file_name):
    """ Get connection details from config file
    Args:
        file_name: name of file on disk including path (relative or absolute)
    Returns:
        a dictionary containing connection details
    """
    
    # Initial empty dictionary to store connection details
    connections = {}

    # Open config file to get connection info
    with open(file_name) as f:
        lines = f.readlines()
        for line in lines:
            # remove all white space (space, tab, new line)
            line = ''.join(line.split())

            # get connection info
            connection_param, connection_value = line.split(":", 1)
            connections[connection_param] = connection_value
    return connections

def main():
    """ Entry point to running the program. Loads a file in the same directory named order_manifest.json, parses the file into SQL INSERT statements, and loads the inventory into the database
    Args:
        None
    Returns:
        Nothing
    """
    with open(SETUPDIR + "/order_manifest.json") as f:
        data = json.load(f)
    
    data, status, exp = validate_manifest(data)
    
    if status:
        # Retrieve connection information from configuration file
        connection_detail = get_connection_info(SETUPDIR + "/connection.config")
        namespace = connection_detail["namespace"]
        os.environ["IRISNAMESPACE"] = namespace
        username = connection_detail["username"]
        os.environ["IRISUSERNAME"] = username
        password = connection_detail["password"]
        os.environ["IRISPASSWORD"] = password

        msg = load_manifest(data)
        if msg:
            print(msg)
    else:
        print(exp)

if __name__ == '__main__':
    main()