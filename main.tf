terraform {
    required_providers {
        azurerm = {
            source = "hashicorp/azurerm"
            version = ">= 3.8"
        }
    }

    backend "azurerm" {
      resource_group_name   = "Cohort31_StuShe_ProjectExercise"
      storage_account_name  = "stushepterraformremstore"
      container_name        = "remote-state"
      key                   = "stu-todoapp-terraform.tfstate"
    }
}

provider "azurerm" {
    features {}
    subscription_id = var.AZURE_SUBSCRIPTION
}

data "azurerm_resource_group" "main" {
    name = var.AZURE_RESOURCE_GROUP
}

resource "azurerm_service_plan" "main" {
    name                    = var.APP_SERVICE_PLAN_NAME
    location                = data.azurerm_resource_group.main.location
    resource_group_name     = data.azurerm_resource_group.main.name
    os_type                 = var.APP_SERVICE_PLAN_OS
    sku_name                = var.APP_SERVICE_PLAN_SKU
}

resource "azurerm_linux_web_app" "main" {
    name                = var.WEB_APP_NAME
    location            = data.azurerm_resource_group.main.location
    resource_group_name = data.azurerm_resource_group.main.name
    service_plan_id     = azurerm_service_plan.main.id

    client_affinity_enabled = true
    https_only = true

    site_config {
        always_on = false
        ftps_state = "FtpsOnly"
        http2_enabled = true
        application_stack {
            docker_image_name = var.DOCKER_IMAGE_NAME
            docker_registry_url = var.DOCKER_REGISTRY_URL
        }
    }

    app_settings = {
        "DB_COLLECTION"                         = var.COSMOSDB_COLLECTION_NAME
        "DB_CONNECTION_STRING"                  = azurerm_cosmosdb_account.db.primary_mongodb_connection_string
        "DB_TABLE"                              = var.COSMOSDB_TABLE_NAME
        "FLASK_APP"                             = var.FLASK_APP
        "FLASK_DEBUG"                           = var.FLASK_DEBUG
        "OAUTH_CLIENT"                          = var.OAUTH_CLIENT
        "OAUTH_SECRET"                          = var.OAUTH_SECRET
        "SECRET_KEY"                            = var.SECRET_KEY
        "WEBSITE_ENABLE_APP_SERVICE_STORAGE"    = var.WEBSITE_ENABLE_APP_SERVICE_STORAGE
        "WEBSITE_PORT"                          = var.WEBSITE_PORT
    }
}

resource "azurerm_cosmosdb_account" "db" {
    name                = "${var.COSMOSDB_ACCOUNT_NAME}"
    location            = data.azurerm_resource_group.main.location
    resource_group_name = data.azurerm_resource_group.main.name
    offer_type          = "Standard"
    kind                = "MongoDB"
    minimal_tls_version = "Tls12"
    mongo_server_version = "4.2"

    automatic_failover_enabled = true

    capabilities {
      name = "EnableServerless"
    }

    capabilities {
      name = "EnableAggregationPipeline"
    }

    capabilities {
      name = "mongoEnableDocLevelTTL"
    }

    capabilities {
      name = "MongoDBv3.4"
    }

    capabilities {
      name = "EnableMongo"
    }

    consistency_policy {
      consistency_level = "Session"
      max_interval_in_seconds = 5
      max_staleness_prefix = 100
    }

    geo_location {
      location = "uksouth"
      failover_priority = 0
    }

    lifecycle {
      prevent_destroy = true
    }
}

resource "azurerm_cosmosdb_mongo_database" "main" {
    name                = var.COSMOSDB_COLLECTION_NAME
    resource_group_name = azurerm_cosmosdb_account.db.resource_group_name
    account_name        = azurerm_cosmosdb_account.db.name

    lifecycle {
      prevent_destroy = true
    }
}

resource "azurerm_cosmosdb_mongo_collection" "main" {
    name                = var.COSMOSDB_TABLE_NAME
    resource_group_name = azurerm_cosmosdb_account.db.resource_group_name
    account_name        = azurerm_cosmosdb_account.db.name
    database_name       = azurerm_cosmosdb_mongo_database.main.name

    index {
        keys = ["_id"]
        unique = true
    }
}
