# Import Packages
from flask import Blueprint, jsonify, request
from enum import Enum
from os import path

# Import db_operations and psycopg2
from config import create_connection, commit_destroy_connection, psycopg2

# Import select_operations
from operations import GET_ALL, GET_SINGLE

# Define Blueprint
item_type = Blueprint('item_type', __name__)

definers = [
    path.basename(__file__)[0:10],
    path.basename(__file__)[0:9]
]

# Get item_types
@item_type.route('/', methods=['GET'])
def get_item_types():
    # Declaration of a List of Records
    list_records = []

    try:
        # Establish the connection and creation of the cursor
        connection = create_connection()
        cur = connection.cursor()

        # Creating the SQL Command
        encoded_command = (
            f"{GET_ALL(definers[0])}")

        cur.execute(encoded_command)

        # Fetching all the records from the cursor
        database_records = cur.fetchall()

        print(database_records)

        # Will store everysingle record in a list formated with a certain format
        for record in database_records:
            dictionary_row = {
                "item_type_Cod": record[0],
                "designation": record[1]
            }
            list_records.append(dictionary_row)

        # Returning the records complete list
        return jsonify({
            "Message": (f"{definers[0]} returned with success!"),
            "Records": list_records
        }), 200

    except (Exception, psycopg2.Error) as error:
        # Convert error to string, break the string on "!"
        error = str(error)
        error = error.split("\n")

        return jsonify({
            "Message": {
                "Message": (f"There was an error getting the {definers[0]}!"),
                "Error": error[0]
            }
        }), 500
    finally:
        # commiting and closing database connection.
        if(connection):
            commit_destroy_connection(connection, cur)

# Get item_type
@item_type.route('/<cod_item_type>', methods=['GET'])
def get_item_type(cod_item_type):
    try:
        # Establish the connection and creation of the cursor
        connection = create_connection()
        cur = connection.cursor()

        # Creating the SQL Command
        encoded_command = (
            f"{GET_SINGLE(definers[1],cod_item_type)}")

        cur.execute(encoded_command)

        # Fetching all the records from the cursor
        database_record = cur.fetchall()

        print(database_record)

        # Returning the records complete list
        return {
            "Message": (f"{definers[1]} returned with success!"),
            "Record": database_record
        }, 200

    except (Exception, psycopg2.Error) as error:

        # Convert error to string, break the string on "!"
        error = str(error)
        error = error.split("\n")

        return jsonify({
            "Message": {
                "Message": (f"There was an error getting the {definers[1]}!"),
                "Error": error[0]
            }
        }), 500
    finally:
        # commiting and closing database connection.
        if(connection):
            commit_destroy_connection(connection, cur)
