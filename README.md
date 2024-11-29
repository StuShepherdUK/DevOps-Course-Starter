# DevOps Apprenticeship: Project Exercise

## Overview

An application created using Python Flask with Poetry to add/modify todo items stored within a database. The application is run within a docker container. The solution uses GitHub for source control and authorization.  The solution is hosted within Microsoft Azure cloud using web app services.  Using GitHub Actions (WebHooks), activated by the source control, deploy to Azure automatically when there are specific updates from the Master Branch. Security is managed using GitHub OAuth service. 

## System Requirements

## Docker

The project uses docker to run the and build the project locally.  Install the appropriate version from their website: https://www.docker.com/

An account will also be required which is referenced during docker builds, i.e. `--tag myaccountname/my-todo-app:latest`

Ensure that any required application within Docker Hub Repository is enabled for `public access`.  This is to ensure Azure can pull the repository into its service.

## Microsoft Azure CLI

The project uses the Microsoft Azure Command Line Interface (CLI) tool. Install the appropriate version from their webiste:  https://learn.microsoft.com/en-us/cli/azure/

Note: Ensure installed Azure CLI is upto date as Microsoft commands can change frequently which can cause commands not to function as expected: `az upgrade`

## Terraform

The project uses Terraform to deploy its cloud solution using Infrastructure As Code (IAC).  Install the appropriate version from their website: https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli

## Python Poetry

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.8+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Poetry installation (PowerShell)
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

###  Poetry Install

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```


## Dependencies

### Python and Poetry Packages

The solution requires additional libraries to be installed for Python and Poetry:

```bash
$ pip install pytest
$ pip install mongomock
$ poetry add pymongo
$ poetry add setuptools
$ poetry add loggly-python-handler
```

### Environment Variables

The solution uses secrets within environment variables to control the application setup. Create copies of `.env.template` to `.env`.

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

Expected output similar to the following:
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
< or >
$ poetry run pytest
```

Expected output similar to the following:
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

*Note: Ensure no secrets are stored within the .env.test file*

## Docker - Build solution locally for testing/development

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

#### Push Docker Image to Docker Hub

1. Login to docker
    - docker login
2. Build the docker image for the docker cloud store
    - docker build --target production --tag `dockerhub_username`/`container-image-name`:latest .
3. Push docker image to the docker cloud store
    - docker push `dockerhub_username`/`container-image-name`:latest
4. View / Ensure docker image pushed correctly by viewing online.
    - Goto https://hub.docker.com/, login and check the container image is available

Note the tag name, this shall be used during the CI/CD pipeline.

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

## Azure Cloud Service

The solution is hosted for public access via Microsoft Azure Cloud service.  Additionally a CosmoDB database is used within Azure to securely store the data used by the solution.

The Azure solution is written using Terraform Infrastructure as Cloud and is contained within the following files:
* main.tf
* output.tf
* variables.tf

If working locally, copy the file `variables.auto.tfvars.template` to `variables.auto.tfvars` and populate all the necessary variable values.

Two variables which are prequesites are the Azure Subscription ID (Account ID) and Resource Group which must be made seperately - Typically by the account Administrator.

Note: The CI/CD pipeline passes the variables in using local environment settings.  This is achieved by the vairable being preced with TF_VAR_, i.e. variable `FLASK_APP` = `TF_VAR_FLASK_APP`

To 'remember' the current state of the deployment, terraform uses state files.  If a remote state is not specified the state file will be saved localled.  Within `main.tf` the remote state is set within the `backend "terraform > "azurerm"` property.  Ensure the the settings here are correct.

If a remote state blob storage container does not exist.  Manually create an Azure Blob storage account within the same resource_group being used.  Within the Blob storage account create a suitable container, for example `remote-state`.  The key value within the remote state must be unique per deployment to avoid overwriting known states.

### Terraform Commands

To run Terraform locally, ensure that the `variables.auto.tfvars` is completed.  Then log into Azure using the Azure CLI tool previously installed, selecting the necessary subscription id.

Additionally, within `main.tf` ensure that the correct backend is referenced within the backend "azurerm" property

```terraform
$ az login 
- Select subscription
$ terraform init
$ terraform plan
```

The plan will validate the cloud state vs local script, compare and identify changes necessary.

```terraform
$ terraform apply
- Runs a plan and asks to confirm before applying changes
$ terraform apply --auto-approve
- Runs a plan and then automatically applys the changes
```

## Azure Infrastructure

The terraform infrastructure creates/manages the following services:
* Service Plan
  * Linux Web App
* CosmosDB Account
  * CosmosDB Mongo Database
    * CosmosDB Mongo Database Collection 

### Azure Mongo DB (CosmosDB) Enryption Notes

Azure CosmosDB by default utilises both Enryption in transit and Encryption at rest. Encryption in transit ensures that secure protocols are always required and utilised when sending/reciving the data. Encryption at rest ensures that the data is secured using a key management system (KMS) and azure specifically, access is granted through the Management Service Resource Provider.  The default generated keys are used as standard however it is possible to add custom-managed keys to the data if required.

## Validating Azure Deployment

A couple of options are available to validate the deployment.

- Terraform output - terraform will state if an apply was successful or not
- Using a web browser goto: http://`webapp_name`.azurewebsites.net/
- View Web App Live Log Stream (Active current connections and activities)
    - Within the Azure Web Portal (https://portal.azure.com/), goto the `Resource`, select the `Web App`, Left-hand Menu -> `Log stream`
- View deployment logs (Ensure docker image being pulled successfully etc.)
    - Within the Azure Web Portal (https://portal.azure.com/), goto the `Resource`, select the `Web App`, Left-hand Menu -> `Deployment` -> `Deployment Center` -> `Logs`

Additional logging is available within the Azure Web Portal (https://portal.azure.com/), goto the `Resource`, select the `Web App` -> Left-Hand Menu -> `Monitoring` section however these have not been enabled within this deployment,


## Webhook for CI/CD steps

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

## Provisioning Role for CI/CD

For a CI/CD process to run infrastructure commands, such as Terraform, a specific provisioning role must be created/enabled for use.

Run the following command using the Azure CLI to provision a specifc role for use, updating the `role_name`, `subscription_id` and `resource_group_name` accordingly

- az ad sp create-for-rbac --name "`role_name`" --role Contributor --scopes /subscriptions/`subscription_id`/resourceGroups/`resource_group_name`

Note the response values, these are needed within the CI/CD pipeline and stored within the GitHub Secrets (See Below)

## GitHub Authorisation / OAuth

The application uses GitHub Authentication through OAuth. The output's from the setup are used within the environment variables file OAUTH_CLIENT and OAUTH_SECRET.  Follow the steps below to setup GitHub Client Authentication:

* Within Github:
  * Click Account Profile, Top-right
    * Select Settings
      * Select <> Developer Settings
  * Select OAuth Apps
    * Click New and add the necessary settings:
      * Application Name:  name
      * Homepage Url:   https://myurl/
      * Authorization callback URl:  https://myurl/login/callback
    * Click Register
  * Within Client secrets section, click to generate a new secret.
    * Note the secret (Only visible once)
    * Note the client Id
    * Store these values in the environment file as necessary (See below, GitHub Secrets and Variables)

## GitHub Secrets and Variables

To utilise secure secrets and variables within the solution, the GitHub repository of code shall never contain any secrets or project specific variables.  These variables should be stored within GitHub Secrets / Variables.

Within GitHub Actions these variables are imported and mapped accordingly for use as necessary (See GitHub Actions below)

1. Within the GitHub Account, Correct Repository
2. Goto Settings
3. Secrets and Variables > Actions
4. Repository Secrets:
    - ARM_CLIENT_ID - `appId` from the Provisioning  Role creation
    - ARM_CLIENT_SECRET - `password` from the Provisioning Role creation
    - ARM_SUBSCRIPTION_ID - Azure Subscription Id
    - ARM_TENANT_ID - `tenant_id` from the Provisioning Role creation
    - AZURE_WEBHOOK - contains the azure webhook url to trigger the Azure pull / deploy function
    - DOCKER_USERNAME - Username for docker account (To enable build/push)
    - DOCKER_PASSWORD - Password for docker account (To enable build/push)
    - TF_VAR_OAUTH_CLIENT - Oauth Client from GitHub Authentication
    - TF_VAR_OAUTH_SECRET - OAuth Secret from GitHub Authentication
    - TF_VAR_SECRET_KEY - Custom secret key for the app to use
5. Repository Variables:
    - TF_VAR_APP_SERVICE_PLAN_NAME - Custom name for App Service Plan
    - TF_VAR_APP_SERVICE_PLAN_OS - OS Value, for example `Linux`
    - TF_VAR_APP_SERVICE_PLAN_SKU - SKU Value, for example `B1`
    - TF_VAR_AZURE_RESOURCE_GROUP - Azure Resource Group (Created in Prequesite)
    - TF_VAR_AZURE_SUBSCRIPTION - Azure Subscription Id (Created in Prequesite)
    - TF_VAR_COSMOSDB_ACCOUNT_NAME - Custom name for CosmoDB
    - TF_VAR_COSMOSDB_COLLECTION_NAME - Custom collection name
    - TF_VAR_COSMOSDB_TABLE_NAME - Custom table name - should match solution requirement
    - TF_VAR_DOCKER_IMAGE_NAME - Docker location / tag of produciton image
    - TF_VAR_DOCKER_REGISTRY_URL - Docker url, for example `https://docker.io`
    - TF_VAR_FLASK_APP - Folder location of flask app, for example `todo_app/app`
    - TF_VAR_FLASK_DEBUG - String value if debug enabled, for example "False"
    - TF_VAR_WEBSITE_ENABLE_APP_SERVICE_STORAGE - String value if app service storage enabled, for example "false"
    - TF_VAR_WEBSITE_PORT - Numeric Port number of docker exposed port, for example: 5000
    - TF_VAR_WEB_APP_NAME - Custom name for web app

## GitHub Actions

The solution uses GitHub Actions located within .github/workflow/`appname`.yml. These actions are run during push/pull requests to the GitHub repository (dependant on the rules applied).

This solution:
* On Push requests, ignores changes to `.md` files
* On Pull requests, ignores changes to `.md` files

* Passes in Environment variables from GitHub Secrets and Variables
  * Variables are mapped to the local system name as necessary to be used by the solution
* On all requests runs `build_and_test_docker`
  * Checks out the trigger repo
  * Builds the docker image for testing
  * Runs the docker image passing in the test environment file
* On push request runs `push_docker_to_prod` - if push and main branch
  * Logs into Docker
  * Checks out the trigger repo
  * Builds the docker image for production
  * Pushes the built image to docker hub
  * Activates the Azure webhook to pull the latest Docker image to Azure
* On push request runs `init_and_apply_infrastructure`
  * Checks out the trigger repo
  * Terraform Init
  * Terraform Plan
  * Terraform Apply - if push and main branch

### Automated Testing - Github Actions

Results of testing GitHub Actions can be found here:

Results for these tests can be found:
- https://github.com/*Account*/*Workspace*/actions





Adding Loggly:

www.loggly.com
Logs -> Customer Tokens -> Add new token -> Set description -> Note secret

install loggly-python-handler using poetry