from flask import Flask, render_template, request, redirect
from todo_app.flask_config import Config

from todo_app.data.trello_items import get_items,add_item,update_item
from todo_app.classes.view_model import ViewModel

app = Flask(__name__)
app.config.from_object(Config())

@app.route('/')
def index():
    all_items = get_items()


    item_view_model = ViewModel(all_items)
    return render_template('index.html', view_model=item_view_model)

    # return render_template('index.html', todoitems=all_items['todo'],doneitems=all_items['done'])

@app.route('/', methods=['POST'])
def addItem():
    newItem = request.form.get('newitem')
    if (newItem != None and newItem.strip() != ''):
        add_item(newItem)
    return redirect('/')

@app.route('/updateItem', methods=['POST'])
def updateItem():
    item_to_update_id = request.form['item_id']
    item_source = request.form['item_source']
    update_item(item_to_update_id,item_source)
    return redirect('/')




