# Core Variables
variable "AZURE_SUBSCRIPTION" {}
variable "AZURE_RESOURCE_GROUP" {}

# App Service Plan
variable "APP_SERVICE_PLAN_NAME" {}
variable "APP_SERVICE_PLAN_OS" {}
variable "APP_SERVICE_PLAN_SKU" {}

# Web App
variable "WEB_APP_NAME" {}
    ## Docker Variables
    variable "DOCKER_IMAGE_NAME" {}
    variable "DOCKER_REGISTRY_URL" {} 
    ## Environment Variables
    variable "DB_COLLECTION" { description = "" }
    variable "DB_TABLE" { description = "" }
    variable "FLASK_APP" { description = "" }
    variable "FLASK_DEBUG" { description = "" }
    variable "OAUTH_CLIENT" { description = "" }
    variable "OAUTH_SECRET" { description = "" }
    variable "SECRET_KEY" { description = "" }
    variable "WEBSITE_ENABLE_APP_SERVICE_STORAGE" { description = "" }
    variable "WEBSITE_PORT" { description = "" }

# CosmoDB
variable "COSMOSDB_ACCOUNT_NAME" {}
variable "COSMOSDB_DATABASE_NAME" {}
variable "COSMOSDB_COLLECTION_NAME" {}