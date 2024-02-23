import pytest
from dotenv import load_dotenv, find_dotenv
import os
import requests

from todo_app.classes.view_model import ViewModel
from todo_app.classes.item_class import Item
from todo_app import app

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    test_app = app.create_app()

    with test_app.test_client() as client:
        yield client

class StubResponse():
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data

    def json(self):
        return self.fake_response_data
    
def stub(url, data, headers, verify):
    trello_boards_url       = "https://api.trello.com/1/boards/"
    trello_board_id         = os.environ.get('TRELLO_BOARD_ID','')
    trello_api_key          = os.environ.get('TRELLO_API_KEY','')
    trello_api_token        = os.environ.get('TRELLO_API_TOKEN','')
    trello_api_security     = "key="+trello_api_key+"&token="+trello_api_token

    get_item_req_url = trello_boards_url+trello_board_id+'/cards/?'+trello_api_security 
    if url == get_item_req_url:
        fake_response_data = [{
            'id': 'test_id_1',
            'name': 'test_todo_item',
            'idList': '658400a6795546f35c80c673'
        },{
            'id': 'test_id_2',
            'name': 'test_done_item',
            'idList': '658400a77be14947511810e0'
        }]
        return StubResponse(fake_response_data)

    raise Exception(f'Integration test did not expect URL "{url}"')


def flatten_html_response(html):
    flatten_rules = {" ":"","\n":""}
    for old,new in flatten_rules.items():
        html=html.replace(old,new)
    return html

def test_index_page(monkeypatch,client):
    monkeypatch.setattr(requests, 'get', stub)

    response = client.get('/')

    assert response.status_code == 200
    assert 'name="item_id" value="test_id_1"' in response.data.decode()
    assert 'name="item_id" value="test_id_2"' in response.data.decode()

    #Specific test to current HTML layout
    assert 'name="item_id"value="test_id_1"><inputtype="hidden"name="item_source"value="todo"' in flatten_html_response(response.data.decode())
    assert 'name="item_id"value="test_id_2"><inputtype="hidden"name="item_source"value="done"' in flatten_html_response(response.data.decode())

