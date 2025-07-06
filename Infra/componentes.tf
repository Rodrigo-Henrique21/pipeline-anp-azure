provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "main" {
  name     = "rg-anp-function"
  location = "East US"
}

resource "azurerm_storage_account" "storage" {
  name                     = "stganpstorage"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_app_service_plan" "plan" {
  name                = "plan-anp"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  kind                = "FunctionApp"
  reserved            = false

  sku {
    tier = "Dynamic"
    size = "Y1"
  }
}

resource "azurerm_application_insights" "ai" {
  name                = "appi-anp"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  application_type    = "web"
}

resource "azurerm_function_app" "func" {
  name                       = "func-anp"
  location                   = azurerm_resource_group.main.location
  resource_group_name        = azurerm_resource_group.main.name
  app_service_plan_id        = azurerm_app_service_plan.plan.id
  storage_account_name       = azurerm_storage_account.storage.name
  storage_account_access_key = azurerm_storage_account.storage.primary_access_key
  version                    = "~4"
  os_type                    = "linux"

  app_settings = {
    FUNCTIONS_WORKER_RUNTIME = "python"
    BLOB_CONN_STR            = azurerm_storage_account.storage.primary_connection_string
    AzureWebJobsStorage      = azurerm_storage_account.storage.primary_connection_string
    APPINSIGHTS_INSTRUMENTATIONKEY = azurerm_application_insights.ai.instrumentation_key
  }
}
