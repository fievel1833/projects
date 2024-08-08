import pymongo
import pandas as pd
import pymongo.errors

"""
This module provides functions for storing data in either a CSV file or a MongoDB database.

Args:
    connection_string (str): The connection string for the MongoDB database.
    database_name (str): The name of the MongoDB database.
    collection_name (str): The name of the MongoDB collection.
"""

connection_string = "mongodb://localhost:27017/"
database_name = 'koi_projects'
collection_name = 'koi_cumulative'

def connect_to_mongodb(connection_string):
    """Connects to the MongoDB database.

    Args:
        connection_string (str): The connection string for the MongoDB database.

    Returns:
        pymongo.MongoClient: A MongoClient object if connected successfully, otherwise None.
    """
    try:
        client = pymongo.MongoClient(connection_string)
        return client
    except (pymongo.errors.ConnectionFailure, pymongo.errors.ServerSelectionTimeoutError, pymongo.errors.AutoReconnect) as e:
        print(f"Error connecting to database: {e}")
        return None

def create_database(client, db_name):
    """Creates a MongoDB database.

    Args:
        client (pymongo.MongoClient): The MongoClient object.
        db_name (str): The name of the database.

    Returns:
        pymongo.database.Database: The created database.
    """
    db = client[db_name]
    return db

def create_collection(db, collection_name):
    """Creates a MongoDB collection.

    Args:
        db (pymongo.database.Database): The database.
        collection_name (str): The name of the collection.

    Returns:
        pymongo.collection.Collection: The created collection.
    """
    collection = db[collection_name]
    return collection

def store_in_database(data, output_path=""):
    """Stores data in either a CSV file or a MongoDB database.

    Args:
        data (list): The data to be stored.
        output_path (str, optional): The path to the CSV file. Defaults to "".
    """
    if output_path != "":
        try:
            record_df = pd.DataFrame(data, columns=["object_name", "host_luminosity", \
                "host_color", "koi_pdisposition", "koi_disposition"])
            record_df.to_csv(output_path, mode="w", header=True, index=False)
        except (IOError, PermissionError, OSError, ValueError, TypeError) as e:
            print(f"Unable to write to file: " + output_path + ": ", e)
    else:
        client = connect_to_mongodb(connection_string)
        if client:
            db = create_database(client, database_name)
            collection = create_collection(db, collection_name)
            collection.insert_many(data)
            client.close()
