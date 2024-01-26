import pytest
from todo_app.classes.view_model import ViewModel
from todo_app.classes.item_class import Item


@pytest.fixture
def test_data():
    items = []
    items.append(Item('id1','item_name_1','done'))
    items.append(Item('id2','item_name_2','todo'))
    items.append(Item('id3','item_name_3','todo'))
    items.append(Item('id4','item_name_4','done'))
    items.append(Item('id5','item_name_5','todo'))
    return items

def test_view_model_done_property_returns_todo_items_only(test_data):
    # arrange
    items = test_data
    view_model = ViewModel(items)
    # act
    filtered_items = view_model.todo_items
    # assert
    assert len(filtered_items) == 3

def test_view_model_done_property_returns_done_items_only(test_data):
    # arrange
    items = test_data
    view_model = ViewModel(items)
    # act
    filtered_items = view_model.done_items
    # assert
    assert len(filtered_items) == 2