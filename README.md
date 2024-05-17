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


### Deploying on Server(s) using Ansible

#### Initial Setup

- Atleast two servers on the same network, one control node, 1+ managed node
  - managed nodes should have internet access enabled for port 5000
- Ability to ssh to control node
  - Access through either:
    - Username / Password
    - Shared SSH key
      - ssh-keygen -t ed25519 -C "you@email.com"
      - ssh-copy-id username@controlnodeip  (ec2-user@1.2.3.4)
- From the control node, setup ability to ssh to the managed nodes
  - Enable access through an SSH Key setup from the control node (Password access can not be used):
    - ssh-keygen -t ed25519 -C "you@email.com"
    - ssh-copy-id username@managednodeip  (ec2-user@1.2.3.4)
- Within the control node, ensure ansible is installed
  - ansible --version
  - if not, install:
    - sudo pip install ansible
- Copy local files from "ansible/home/ec2-user" to the control node "/home/ec2-user" path
    - .env.j2
    - configure_webservers.yml
    - controlled_nodes.ini
    - todoapp.service

- Ensure that the managed nodes are correctly listed within controlled_nodes.ini

```
    [webservers]
    managednodeip1
    managednodeip2
    managednodeipx
```

#### Running Ansible

- Within the control node:
  - cd /home/ec2-user
  - ansible-playbook configure_webservers.yml -i controlled_nodes.ini
- Ensure that there are no errors
- navigate to any host ip address in a public web browser:
  - http://managednodeip:5000




## Deploying on Server(s) using Docker

### Notes for Corporate Proxy Configuration

Docker when running behind corporate proxy may require a proxy set within the Docker app itself to enable package connectivity and then proxy config setting to enable internal internet access to the docker image.

Install local proxy as normal, opening localhost:3128

Within Windows Docker, Add proxy settings:
- Web Serer (HTTP) = http://localhost:3128
- Web Server (HTTPS) = http://localhost:3128
- BYpass proxy settings for these hosts & domains =  localhost,127.0.0.1,.CORPNAMEHERE.com

Within Docker config file add proxy settings:
C:\Users\<user>\.docker\config.json

"proxies":
 {
   "default":
   {
     "httpProxy": "http://host.docker.internal:3128",
     "httpsProxy": "http://host.docker.internal:3128",
     "noProxy": "host.docker.internal,localhost,127.0.0.1,.CORPNAMEHERE.com"
   }
 }

### Docker Commands

#### Build

Build the relevant environment (dev / prod / test) using the following commands:
- docker build --target development --tag todo-app:dev .
- docker build --target test --tag todo-app:test .
- docker build --target production --tag todo-app:prod .


#### Run

Run the docker project in the relevant environment (dev / prod) using the following commands:
- dev:
  - Live Edit of Files:
      - docker run -ti --mount type=bind,source="$(pwd)/todo_app",target=/opt/todoapp/todo_app  -p 5000:5000 --env-file .env -d todo-app:dev
  - Static Files:
      - docker run -ti -p 5000:5000 --env-file .env -d todo-app:dev
- test:
  - docker run -ti -p 5000:5000 --env-file .env -d todo-app:test
- prod:
  - docker run -ti -p 5000:5000 --env-file .env -d todo-app:prod

*Note: Within windows, $(pwd) only works with powershell not cmd/dos.  Cmd/dos requires %cd%*

After running, the application will be available locally via any webbrowser:
- http://127.0.0.1:5000/

Command Breakdown:
- --mount type=bind,source="$(pwd)/todo_app",target=/opt/todoapp/todo_app
  - mounts the localpath/todo_app to /opt/todoapp/todo_app as a binded folder within the docker container for realtime changes
- -p 5000:5000
  - Maps the port 5000 to internal port 5000 where the app shall be hosted
- --env-file .env
  - Identify which environment file should be used by the docker container
- -d
  - Run environment detached (in background)
- todo-app:dev
  - container (todo-app) and version (dev) to run

#### Additional useful Docker commands

- -d (without)
  - Docker run without using -d will run the docker container in the current shell/bash terminal
- -it (used without -d)
  - Launch interactive terminal when developing/testing
- docker run --help
  - View other docker run help commands
- docker ps
  - View running containers
- docker exec -it abcdefghijk bash
  - Access terminal of a running container, where abcdefghijk is the container ID (obtained from docker ps command)



### Automated Testing - Github Actions

Associated with this workspace are github actions (within .github/workflows/) which, upon any push or pull from the github repository will build the docker test container and run the docker test image to ensure tests are all passing.

Results for these tests can be found:
- https://github.com/*Account*/*Workspace*/actions
- https://github.com/StuShepherdUK/DevOps-Course-Starter/actions