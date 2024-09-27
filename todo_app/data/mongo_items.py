from datetime import datetime,timezone
from bson.objectid import ObjectId
from flask import session
from todo_app.classes.item_class import Item
import json
import pymongo
import os
import requests
import uuid

"""
    IMPORTANT - Due to work environment and working localhost, requests api causes SSL error
    Therefore verify=False is necessary on requests call as a work-around
"""

def get_items():
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of saved items.
    """

    try:
        db_connectionstring = os.environ.get('DB_CONNECTION_STRING','')
        db_collection = os.environ.get('DB_COLLECTION','')
        db_table = os.environ.get('DB_TABLE','')
        
        db_client = pymongo.MongoClient(db_connectionstring)
        db = db_client[db_collection]
        
        all_items = []
        for item in db[db_table].find():
            all_items.append(Item(
                        ObjectId(item.get('_id','')),
                        item.get('name',''),
                        item.get('status','')
                    ))

        return_items = all_items
        session.clear()
        return return_items

    except Exception as e:
        print("An error occurred during get_items:", e)
        return []


def add_item(title):

    try:
        db_connectionstring = os.environ.get('DB_CONNECTION_STRING','')
        db_collection = os.environ.get('DB_COLLECTION','')
        db_table = os.environ.get('DB_TABLE','')

        db_client = pymongo.MongoClient(db_connectionstring)
        db = db_client[db_collection]
        
        item_to_add = {
             "name":title
            ,"created":datetime.now(tz=timezone.utc)
            ,"modified":datetime.now(tz=timezone.utc)
            ,"status":"todo"
        }
        db[db_table].insert_one(item_to_add).inserted_id
        get_items()
        return item_to_add
    except Exception as e:
        print("An error occurred during add_item:", e)
        return {}


def update_item(item_to_update_id,previous_status):

    try:

        db_connectionstring = os.environ.get('DB_CONNECTION_STRING','')
        db_collection = os.environ.get('DB_COLLECTION','')
        db_table = os.environ.get('DB_TABLE','')
        
        db_client = pymongo.MongoClient(db_connectionstring)
        db = db_client[db_collection]
        
        target_status = 'todo'
        if previous_status == 'todo':
            target_status = 'done'

        update_item = { "status":target_status, "modified":datetime.now(tz=timezone.utc)}
        
        db[db_table].update_one({"_id":item_to_update_id}, {"$set": update_item})
        
        get_items()
        return update_item

    except Exception as e:
        print("An error occurred during update_item:", e)
        return {}

