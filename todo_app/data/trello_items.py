from flask import session
from ..classes.item_class import Item
import json
import os
import requests
import uuid

"""
    IMPORTANT - Due to work environment and working localhost, requests api causes SSL error
    Therefore verify=False is necessary on requests call as a work-around
"""

allItems = Item()

trello_boards_url       = "https://api.trello.com/1/boards/"
trello_cards_url        = "https://api.trello.com/1/cards"
trello_board_id         = os.environ.get('TRELLO_BOARD_ID','')
trello_board_list_id_todo = os.environ.get('TRELLO_BOARD_LIST_ID_TODO','')
trello_board_list_id_done = os.environ.get('TRELLO_BOARD_LIST_ID_DONE','')
trello_api_key          = os.environ.get('TRELLO_API_KEY','')
trello_api_token        = os.environ.get('TRELLO_API_TOKEN','')
trello_api_security     = "key="+trello_api_key+"&token="+trello_api_token
trello_default_get_header   = {"Accept": "*/*"}
trello_default_put_header   = {"Accept": "application/json"}
trello_default_post_header   = {"Accept": "application/json"}
cards_status_options    = ['all','closed','none','open','visible']

def get_items():
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of saved items.
    """
    get_item_req_url = trello_boards_url+trello_board_id+'/cards/?'+trello_api_security 
    response = requests.request("GET", get_item_req_url, data='',  headers=trello_default_get_header, verify=False)
    response_json = response.json()
    
    todo_items = []
    done_items = []

    for item in response_json:
        if item.get('idList','') == trello_board_list_id_todo:
            todo_items.append(item)
        elif item.get('idList','') == trello_board_list_id_done:
            done_items.append(item)                
    return_items = {'todo':todo_items,'done':done_items}
    session.clear()
    return session.get('items', return_items.copy())


def add_item(title):
    """
    Adds a new item with the specified title/name to the session.

    Args:
        name: The name of the item.
        idList: The ID of the List to add the card
        key: API Key
        token: API T oken
        
    Returns:
        item: The saved item.
    """
    # items = get_items()

    # headers = {"Accept": "application/json"}
    query = {
        'idList':   trello_board_list_id_todo,
        'key':      trello_api_key,
        'token':    trello_api_token,
        'name':     title
    }
    response = requests.request("POST",trello_cards_url,headers=trello_default_post_header,params=query,verify=False)
    print("ADD ITEM RESPONSE:", response)


    get_items()
    # items['todo'].append(query)
    # session['items'] = items

    return query


def update_item(item_to_update_id,source):

    if source.lower() == "todo":
        target_list = trello_board_list_id_done
    elif source.lower() == "done":
        target_list = trello_board_list_id_todo

    update_item_url = trello_cards_url+'/'+item_to_update_id+'?idList='+target_list

    query = {
        'key':      trello_api_key,
        'token':    trello_api_token
    }

    response = requests.request("PUT",update_item_url,headers=trello_default_put_header,params=query,verify=False)
    print("UPDATE ITEM RESPONSE:", response)

    get_items()

    return query

