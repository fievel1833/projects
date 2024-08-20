import pymongo
import pandas as pd

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
            print(f"Unable to write to file: {output_path}: ", e)
    else:
        try:
            client = pymongo.MongoClient(connection_string)
            db = client[database_name]
            collection = db[collection_name]
            collection.insert_many(data)
        except (pymongo.errors.ConnectionFailure, pymongo.errors.ServerSelectionTimeoutError, pymongo.errors.AutoReconnect) as e:
            print(f"Error connecting to database: {e}")
        finally:
            if client:
                client.close()