from datetime import datetime, timezone
from dotenv import load_dotenv, find_dotenv
from bson.objectid import ObjectId
import logging
import mongomock
import os
import pytest
import pymongo


from todo_app.classes.view_model import ViewModel
from todo_app.classes.item_class import Item
from todo_app import app

logger = logging.getLogger(__name__)

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    with mongomock.patch(servers=(('fakemongo.com',27017),)):

        test_app = app.create_app()
        with test_app.test_client() as client:
            yield client

class StubResponse():
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data

    def json(self):
        return self.fake_response_data


def flatten_html_response(html):
    flatten_rules = {" ":"","\n":""}
    for old,new in flatten_rules.items():
        html=html.replace(old,new)
    return html

def test_index_page(monkeypatch,client):
    
    db_connectionstring = os.environ.get('DB_CONNECTION_STRING','')
    db_collection = os.environ.get('DB_COLLECTION','')
    db_table = os.environ.get('DB_TABLE','')

    db_client = pymongo.MongoClient(db_connectionstring)

    db = db_client[db_collection]
    
    test_items = [
        {"name":"giraffe_item","status":"todo"}
        ,{"name":"elephant_item","status":"done"}
        ]
    for item in test_items:
        item_to_add = {
             "name":item['name']
            ,"status":item['status']
        }
        added_id = db[db_table].insert_one(item_to_add).inserted_id
        item['_id'] = added_id

    for item in test_items:
        result = db[db_table].find_one({"_id":item['_id']})
        assert (result['name']==item['name'])

    response = client.get('/')
    assert response.status_code == 200

    for item in test_items:
        logger.info("Test Item: " + str(item['name']))
        assert item['name'] in flatten_html_response(response.data.decode())

    
  