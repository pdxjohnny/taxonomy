import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['taxonomy-database']
coll = db['taxonomy-collection']
