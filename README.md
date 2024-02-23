# DevOps Apprenticeship: Project Exercise

> If you are using GitPod for the project exercise (i.e. you cannot use your local machine) then you'll want to launch a VM using the [following link](https://gitpod.io/#https://github.com/CorndelWithSoftwire/DevOps-Course-Starter). Note this VM comes pre-setup with Python & Poetry pre-installed.

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.8+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.


## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.


## Testing the App

Once all the dependancies have been installed, start testing by running:
```bash
$ pytest
```

You should see output similar to the following:
```bash
* ====== test session starts ======
* platform win32 -- Python 3.xx.x, pytest-x.x.x, pluggy-x.x.x
* rootdir: C:\xxxx\xxxx\xxxx
* collected n items
* 
* todo_app\classes\test_view_model.py
*
* ====== n passes in X.XXs ======
```

In the event of an error and the testing failing:
* Name of test which has failed shall be displayed
* Functional code of test which failed shall be displayed
* A summary shall be displayed detailing the assetation failure

Summary example where the assert value of 3 was incorrect and the value of 2 was returned by the function:
```bash
* ====== short test summary info ======
* FAILED todo_app/classes/test_view_model.py::test_view_model_done_property_returns_done_items_only - assert 2 == 3
* ====== 1 failed, 1 passed in x.xxs ======
```

### Current Tests Available
* Unit Tests
  * tests/test_view_model
    * test_view_model_done_property_returns_done_items_only  
    * test_view_model_todo_property_returns_todo_items_only
* Integration Tests
  * tests/test_app_client
    * test_index_page

### Test Dependencies
Integration tests are set to use the test environment file .env.test instead of the main applications .env file

Updates to any environment variables must be updated here along side the core environment files to maintain testing functionality

*Note: Ensure no secrets are stored within the .env.test file*