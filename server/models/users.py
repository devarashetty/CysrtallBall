from bson.json_util import dumps
def getUsersList(mongo):
    return dumps(mongo.db.users.find())