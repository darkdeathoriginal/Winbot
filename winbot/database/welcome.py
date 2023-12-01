import pymongo
import certifi
ca = certifi.where()
from dotenv import load_dotenv
from winbot.config import database_name,database_url
load_dotenv()

dbclient = pymongo.MongoClient(database_url,tlsCAFile=ca)
database = dbclient[database_name]

welcome_collection = database['welcome']


async def addWelcome(groupId,text):
    fdata = {'id': groupId}
    found = welcome_collection.find_one(fdata)
    if found:
        welcome_collection.delete_one(fdata)

    data = {'id': groupId, 'text':str(text)}
    welcome_collection.insert_one(data)

async def get_all_welcome():
    query = welcome_collection.find().sort('text', 1)
    return query

async def del_all():

    try:
        welcome_collection.remove()
    except:
        return

async def findWelcome(id):
    query = {'id':id}
    
    found = welcome_collection.find_one(query)
    return found
