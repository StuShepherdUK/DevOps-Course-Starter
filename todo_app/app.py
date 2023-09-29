from flask import Flask, render_template, request, redirect
from todo_app.flask_config import Config

# Import session item functions
from todo_app.data.session_items import get_items, add_item

app = Flask(__name__)
app.config.from_object(Config())

# Main URL Homepage
@app.route('/')
def index():
    # Render index.html using todo list items
    return render_template('index.html', todoitems=get_items())

# Main URL Homepage Form Submit
@app.route('/', methods=['POST'])
def addItem():
    # Get Form item 'newitem'
    newItem = request.form.get('newitem')
    # Validate newItem has content
    if (newItem != None and newItem.strip() != ''):    add_item(newItem)
    # Redirect to Main URL Homepage
    return redirect('/')
