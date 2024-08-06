import pymongo

connection_host = 'localhost'
connection_port = 27017

def connect_to_mongodb(host = connection_host, port = connection_port):
    client = pymongo.MongoClient(host, port)
    return client

def create_database(client, db_name):
    db = client[db_name]
    return db

def create_collection(db, collection_name):
    collection = db[collection_name]
    return collection

