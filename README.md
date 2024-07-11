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


## Deploying on Server(s) onto Azure Cloud Platform

### Prequesits

#### Docker Hub

Ensure access to a public docker hub repository - Azure will require public access to pull the container from the repository

#### Azure Resources

Ensure access to an Active Azure account with an existing resource group with the necessary permissions to create cloud components within.

As part of the deployment, resource names will be required to populate the Azure command line scripts, ensure these are understood and note them down:

- `resource_group_name` = My_Resource_Group
- `appservice_plan_name` = My_Todoapp_Appserviceplan
- `webapp_name` = My-Todo-App
- `dockerhub_username` = dockerusername
- `container-image-name` = dockercontainerimagename

Note: These reference names will be referenced below within the command line call's where necessary and should be replaced with their suitable value

#### Environment Variables

You'll also need to clone a new `.env.json` file from the `.env.json.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.json.template .env.json  # (first time only)
```

The `.env.json` file is used by the azure command line tools to push the environment variables to the App Service - Web App.  Ensure that the environment variables are correct.

#### Local CLI Tools

Ensure the following local CLI tools are installed and available:
- Docker
    - Typically installed with local docker application
- Azure CLI
    - See: https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-windows?tabs=azure-cli

Note: Ensure installed Azure CLI is upto date as Microsoft commands can change frequently which can cause commands not to function as expected: `az upgrade`

### Deployment Steps

These steps are all run via a command prompt, if in windows, recommend GitBash command prompt.  (Possibily some commands may not function as excepted in a DOS or PowerShell prompt)

#### Push Docker Image to Docker Hub

1. Login to docker
    - docker login
2. Build the docker image for the docker cloud store
    - docker build --target production --tag `dockerhub_username`/`container-image-name`:latest .
3. Push docker image to the docker cloud store
    - docker push `dockerhub_username`/`container-image-name`:latest
4. View / Ensure docker image pushed correctly by viewing online.
    - Goto https://hub.docker.com/, login and check the container image is available

#### Azure Deployment

5. Login to Azure
    - az login
6. Create an app service plan to host the web application:
    - az appservice plan create --resource-group `resource_group_name` -n `appservice_plan_name` --sku B1 --is-linux
7. Create a web app within the app service plan, linked to the docker image:
    -az webapp create --resource-group `resource_group_name` --plan `appservice_plan_name` --name `webapp_name` --deployment-container-image-name docker.io/`dockerhub_username`/`container-image-name`:latest
8. Push variables from `env.json` to the webapp
    - az webapp config appsettings set -g `resource_group_name` -n `webapp_name` --settings @env.json

The above steps have created an application service plan to host the web application.  The web application is set to pull the docker image from docker hub and apply the environment settings during run.

9. Check website:
    - http://`webapp_name`.azurewebsites.net/

Note: First run of the site or after the site has not been used for a period of time, may take a short period to launch. 

### Deployment Debug

If any of the steps fail within Azure there are a couple of places to check for logs:

1. View Web App Live Log Stream (Active current connections and activities)
    - Within the `Web App`, Left-hand Menu -> `Log stream`
2. View deployment logs (Ensure docker image being pulled successfully etc.)
    - Within the `Web App`, Left-hand Menu -> `Deployment` -> `Deployment Center` -> `Logs`

Additional logging is available within the `Web App` -> Left-Hand Menu -> `Monitoring` section however these have not been enabled within this deployment,

### Webhook for CI/CD steps

To add in CI/CD, web hooks to the web application are required.  Within the Azure Portal within a web browser:
- Goto the App Service
  - Goto Deployment -> Deployment Center
    - Get the webhook URL secret.  This contains:
      - deployment_username
      - deployment_password
      - webapp_name

Important: The default webhook starts with `https://$`.   When using tools such as curl in windows it is important to 'escape' the $ sign by adding a single back-slash in front ( \ ) 

Test the webhook using curl:
-  curl -dH -X POST "https://\\$`deployment_username`:`deployment_password`@`webapp_name`.scm.azurewebsites.net/docker/hook"

A successful test will respond with a JSON object containing the OperationId and TrackingUrl for the logstream

```json
{
"OperationId":"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
,"TrackingUrl":"https://webapp_name_here.scm.azurewebsites.net/api/logstream?filter=op:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx,volatile:false"
}
```

### Automated pipeline between Git, Docker and Azure

A GitHub Workflow job 'push_to_prod' is included within github actions workflow (./github/workflows) where by any push to the main branch will, after a successful test ('build_and_test' job), automatically push a docker build using production criteria and latest tag to Docker Hub. After this the Azure webhook is called, linked to the Docker Hub which will pull the latest build and deploy into the Azure Web App service. The docker credentials and azure webhook are stored as secrets within the GitHub repository.


#### Git Hub Secrets

1. Within the GitHub Account, Correct Repository
2. Goto Settings
3. Secrets and Variables > Actions
4. Repository Secrets:
    - DOCKER_USERNAME - Username for docker account (To enable build/push)
    - DOCKER_PASSWORD - Password for docker account (To enable build/push)
    - AZURE_WEBHOOK - contains the azure webhook url to trigger the Azure pull / deploy function


