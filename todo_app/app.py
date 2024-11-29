from flask import Flask, render_template, request, redirect
from todo_app.flask_config import Config

from todo_app.data.mongo_items import get_items,add_item,update_item
from todo_app.classes.view_model import ViewModel

from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user
import json
import os
import requests


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    app.config['LOGIN_DISABLED'] = os.getenv('LOGIN_DISABLED') == 'True'

    login_manager = LoginManager()
    @login_manager.unauthorized_handler
    def unauthenticated():
        return app.redirect('https://github.com/login/oauth/authorize?client_id='+os.environ.get('OAUTH_CLIENT'))

    @login_manager.user_loader
    def load_user(user_id):
        print("Load User...",user_id)
        return User(user_id)

    login_manager.init_app(app)

    @app.route('/login/callback')
    def login_callback():
        authCode = request.args.get('code')
        
        parameters = {
            'client_id':os.environ.get('OAUTH_CLIENT'),
            'client_secret':os.environ.get('OAUTH_SECRET'),
            'code':authCode
        }
        headers = {'accept':'application/json'}
        result = requests.post('https://github.com/login/oauth/access_token',params=parameters,headers=headers)
        access_token = json.loads(result.content)
  
        headers = {'Authorization':'Bearer '+access_token.get('access_token','missing')}
        user_details = requests.get('https://api.github.com/user', headers=headers)    
        
        userDetails = json.loads(user_details.content)
        CurrentUser = User(userDetails.get('id'))
        
        login_user(CurrentUser)
        return redirect('/')


    class User(UserMixin):
        def __init__(self,id):
            self.id = id

    @app.route('/')
    @login_required
    def index():
        all_items = get_items()
        item_view_model = ViewModel(all_items)
        return render_template('index.html', view_model=item_view_model)

    @app.route('/', methods=['POST'])
    @login_required
    def addItem():
        newItem = request.form.get('newitem')
        if (newItem != None and newItem.strip() != ''):
            add_item(newItem)
        return redirect('/')

    @app.route('/updateItem', methods=['POST'])
    @login_required
    def updateItem():
        item_to_update_id = request.form['item_id']
        item_source = request.form['item_source']
        update_item(item_to_update_id,item_source)
        
        return redirect('/')

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect('/')

    return app
