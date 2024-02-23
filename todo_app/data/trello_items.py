from flask import session
from todo_app.classes.item_class import Item
import json
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
        trello_boards_url       = "https://api.trello.com/1/boards/"
        trello_board_id         = os.environ.get('TRELLO_BOARD_ID','')
        trello_api_key          = os.environ.get('TRELLO_API_KEY','')
        trello_api_token        = os.environ.get('TRELLO_API_TOKEN','')
        trello_api_security     = "key="+trello_api_key+"&token="+trello_api_token
        trello_default_get_header   = {"Accept": "*/*"}
        trello_board_list_id_todo = os.environ.get('TRELLO_BOARD_LIST_ID_TODO','')
        trello_board_list_id_done = os.environ.get('TRELLO_BOARD_LIST_ID_DONE','')
        
        get_item_req_url = trello_boards_url+trello_board_id+'/cards/?'+trello_api_security 
        
        try:
            response = requests.get(get_item_req_url, data='',  headers=trello_default_get_header, verify=False)
        except:
            response = requests.get(get_item_req_url, data='',  headers=trello_default_get_header)

        response_json = response.json()
        print(response_json)
        all_items = []

        for item in response_json:
            if item.get('idList','') == trello_board_list_id_todo:
                all_items.append(Item(
                        item.get('id',''),
                        item.get('name',''),
                        'todo'
                    ))

            elif item.get('idList','') == trello_board_list_id_done:
                all_items.append(Item(
                        item.get('id',''),
                        item.get('name',''),
                        'done'
                    ))

        return_items = all_items
        session.clear()
        return return_items
    except Exception as e:
        print("An error occurred during get_items:", e)
        return []


def add_item(title):

    try:
        trello_cards_url        = "https://api.trello.com/1/cards"
        trello_board_list_id_todo = os.environ.get('TRELLO_BOARD_LIST_ID_TODO','')
        trello_api_key          = os.environ.get('TRELLO_API_KEY','')
        trello_api_token        = os.environ.get('TRELLO_API_TOKEN','')
        trello_default_post_header   = {"Accept": "application/json"}


        query = {
            'idList':   trello_board_list_id_todo,
            'key':      trello_api_key,
            'token':    trello_api_token,
            'name':     title
        }
        try:
            requests.post(trello_cards_url,headers=trello_default_post_header,params=query,verify=False)
        except:
            requests.post(trello_cards_url,headers=trello_default_post_header,params=query)

        get_items()
        return query
    except Exception as e:
        print("An error occurred during add_item:", e)
        return {}


def update_item(item_to_update_id,source):

    try:
        trello_cards_url        = "https://api.trello.com/1/cards"
        trello_board_list_id_todo = os.environ.get('TRELLO_BOARD_LIST_ID_TODO','')
        trello_board_list_id_done = os.environ.get('TRELLO_BOARD_LIST_ID_DONE','')
        trello_api_key          = os.environ.get('TRELLO_API_KEY','')
        trello_api_token        = os.environ.get('TRELLO_API_TOKEN','')
        trello_default_put_header   = {"Accept": "application/json"}

        if source.lower() == "todo":
            target_list = trello_board_list_id_done
        elif source.lower() == "done":
            target_list = trello_board_list_id_todo
        update_item_url = trello_cards_url+'/'+item_to_update_id+'?idList='+target_list
        query = {
            'key':      trello_api_key,
            'token':    trello_api_token
        }
        try:
            response = requests.put(update_item_url,headers=trello_default_put_header,params=query,verify=False)
        except:
            response = requests.put(update_item_url,headers=trello_default_put_header,params=query)
        get_items()
        return query
    except Exception as e:
        print("An error occurred during update_item:", e)
        return {}

