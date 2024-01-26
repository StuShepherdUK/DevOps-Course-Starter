import pytest
from dotenv import load_dotenv, find_dotenv

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

@pytest.fixture
def test_data():
    items = []
    items.append(Item('id1','item_name_1','done'))
    items.append(Item('id2','item_name_2','todo'))
    items.append(Item('id3','item_name_3','todo'))
    items.append(Item('id4','item_name_4','done'))
    items.append(Item('id5','item_name_5','todo'))
    return items

def test_view_model_done_property_returns_done_items_only(client,test_data):
    # arrange
    items = test_data
    view_model = ViewModel(items)
    # act
    filtered_items = view_model.done_items
    # assert
    assert len(filtered_items) == 2

def test_view_model_todo_property_returns_todo_items_only(client,test_data):
    # arrange
    items = test_data
    view_model = ViewModel(items)
    # act
    filtered_items = view_model.todo_items
    # assert
    assert len(filtered_items) == 3