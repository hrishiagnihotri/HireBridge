from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient

#currently using local db,URI to be changed to cluster later
mongo_uri="mongodb://localhost:27017/"

connect=MongoClient(mongo_uri)             #!REMINDER,shift to async io from motor from mongoclient
conn=connect.project50.sienna

conn2=connect.project50.zephyr


conn3=connect.project50.orion
