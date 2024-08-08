import pymongo

connection_host = 'localhost'
connection_port = 27017
database_name = 'koi_cumulative'
collection_name = 'kepler_projects'

def connect_to_mongodb(host = connection_host, port = connection_port):
    client = pymongo.MongoClient(host, port)
    return client

def create_database(client, db_name):
    db = client[db_name]
    return db

def create_collection(db, collection_name):
    collection = db[collection_name]
    return collection

def store_data(data):
    try:
        client = connect_to_mongodb(connection_host, connection_port)
        db = create_database(client, database_name)
        collection = create_collection(db, collection_name)
        collection.insert_one(data)
        client.close()
        
    except Exception as e:
        raise Exception("Unable to connect: ", e)