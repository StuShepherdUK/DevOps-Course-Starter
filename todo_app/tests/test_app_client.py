import pytest
from dotenv import load_dotenv, find_dotenv
import os
import requests

from todo_app.classes.view_model import ViewModel
from todo_app.classes.item_class import Item
from todo_app import app

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    # Create the new app.
    test_app = app.create_app()

    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client

def test_index_page(monkeypatch,client):
    monkeypatch.setattr(requests, 'get', stub)

    response = client.get('/')


class StubResponse():
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data

    def json(self):
        return self.fake_response_data
    
def stub(url, params={}):



    trello_boards_url       = "https://api.trello.com/1/boards/"
    trello_board_id         = os.environ.get('TRELLO_BOARD_ID','')
    trello_api_key          = os.environ.get('TRELLO_API_KEY','')
    trello_api_token        = os.environ.get('TRELLO_API_TOKEN','')
    trello_api_security     = "key="+trello_api_key+"&token="+trello_api_token

    
    get_item_req_url = trello_boards_url+trello_board_id+'/cards/?'+trello_api_security 
    #if url == f'https://api.trello.com/1/boards/{test_board_id}/cards/':
    if url == get_item_req_url:
        fake_response_data = [{
            'id': '123abc',
            'name': 'To Do',
            'idList': '658400a6795546f35c80c673'
        }]
        return StubResponse(fake_response_data)

    raise Exception(f'Integration test did not expect URL "{url}"')