import pymongo
import pandas as pd

connection_string = "mongodb://localhost:27017/"  # Replace with your connection string if needed
database_name = 'koi_projects'
collection_name = 'koi_cumulative'

def connect_to_mongodb(connection_string):
    try:
        client = pymongo.MongoClient(connection_string)
        return client
    except pymongo.errors.ConnectionFailure as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

def create_database(client, db_name):
    db = client[db_name]
    return db

def create_collection(db, collection_name):
    collection = db[collection_name]
    return collection

def store_in_database(data, output_path = ""):
    if output_path != "":
        record_df = pd.DataFrame(data, columns=["object_name", "host_luminosity", "host_color", "koi_pdisposition", "koi_disposition"])
        record_df.to_csv(output_path, mode="w", header=True, index=False)
    else:
        client = connect_to_mongodb(connection_string)
        if client:
            db = create_database(client, database_name)
            collection = create_collection(db, collection_name)
            collection.insert_many(data)
            client.close()
