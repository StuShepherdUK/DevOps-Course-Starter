# Core Variables
variable "AZURE_SUBSCRIPTION" {
            description = "Azure subscription id"
            sensitive = true
        }
variable "AZURE_RESOURCE_GROUP" {
            description = "Azure resource group previously created"
        }

# App Service Plan
variable "APP_SERVICE_PLAN_NAME" {
            description = "Azure App Service Plan Name"
        }
variable "APP_SERVICE_PLAN_OS" {
            description = "App Service Plan OS, i.e. Linux"
        }
variable "APP_SERVICE_PLAN_SKU" {
            description = "App Service Plan SKU, i.e. B1"
        }

# Web App
variable "WEB_APP_NAME" {
            description = "Azure Web App Name"
        }
    ## Docker Variables
    variable "DOCKER_IMAGE_NAME" {
            description = "Docker Image, i.e. name/app:latest"
        }
    variable "DOCKER_REGISTRY_URL" {
            description = "Docker Image location, i.e. https://docker.io"
        } 
    ## Environment Variables
    variable "FLASK_APP" {
            description = "Python Flask App Location, i.e. appfolder/app"
        }
    variable "FLASK_DEBUG" {
            description = "Enable Python Flask Debug, i.e. TRUE/FALSE"
        }
    variable "OAUTH_CLIENT" { 
            description = "GitHub OAuth Apps - Client ID"
            sensitive = true
        }
    variable "OAUTH_SECRET" {
            description = "GitHub OAuth Apps - Client Secret"
            sensitive = true
        }
    variable "SECRET_KEY" {
            description = "Python Flask Secret Key"
            sensitive = true
        }
    variable "WEBSITE_ENABLE_APP_SERVICE_STORAGE" {
            description = "Enable Web App Service Storage"
        }
    variable "WEBSITE_PORT" {
            description = "Python Flask / Docker Hosted Port number"
        }

# CosmoDB
variable "COSMOSDB_ACCOUNT_NAME" {
            description = "Azure CosmosDB Name"
        }
variable "COSMOSDB_COLLECTION_NAME" {
            description = "Azure CosmosDB Collection Name (Database)"
        }
variable "COSMOSDB_TABLE_NAME" {
            description = "Azure CosmosDB Table Name (Within Collection)"
        }