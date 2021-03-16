provider "azurerm" {
  features {}
}

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "2.50.0"
    }
    null = {
      source = "hashicorp/null"
    }
  }
}
resource "azurerm_resource_group" "rsrc_grp" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_virtual_network" "v_net" {
  name                = var.vnet_name
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.rsrc_grp.location
  resource_group_name = azurerm_resource_group.rsrc_grp.name
}

resource "azurerm_subnet" "sub_net" {
  name                = var.subnet_name
  resource_group_name = azurerm_resource_group.rsrc_grp.name
  address_prefixes    = ["10.0.1.0/24"]
  virtual_network_name = azurerm_virtual_network.v_net.name

  enforce_private_link_endpoint_network_policies  = false
  enforce_private_link_service_network_policies   = false
}

resource "azurerm_subnet" "sub_net2" {
  name                = var.subnet2_name
  resource_group_name = azurerm_resource_group.rsrc_grp.name
  address_prefixes    = [var.subnet-2-addr_prefix]
  virtual_network_name = azurerm_virtual_network.v_net.name

  enforce_private_link_endpoint_network_policies  = false
  enforce_private_link_service_network_policies   = false
}
/*
resource "null_resource" "pska" {
  provisioner "local-exec" {
    command = "az network vnet subnet update --name ${var.subnet_name} --resource-group ${var.resource_group_name} --vnet-name ${var.vnet_name} --disable-private-link-service-network-policies true; az network vnet subnet update --name ${var.subnet_name} --resource-group ${var.resource_group_name} --vnet-name ${var.vnet_name} --disable-private-endpoint-network-policies true"
  }
}
*/

#Create storage account.
resource "azurerm_storage_account" "store_acct" {
  name                      = var.storage_acct_name
  location                  = azurerm_resource_group.rsrc_grp.location
  resource_group_name       = azurerm_resource_group.rsrc_grp.name
  account_tier              = var.account_tier
  account_replication_type  = var.account_replication_type
  enable_https_traffic_only = true
  account_kind              = var.account_kind
  access_tier               = var.access_tier
  is_hns_enabled            = false
  min_tls_version           = var.min_tls_version
  allow_blob_public_access  = var.allow_blob_public_access  
  
  identity {
    type = "SystemAssigned"
  }
 /*
  custom_domain {
    name = var.domain_name    
  }
*/
  blob_properties {
    delete_retention_policy {
      days = var.delete_retention_days
    }
  }
  /*
  network_rules {
    default_action             = "Deny"
    bypass                     = ["AzureServices"] 
    ip_rules                   = ["198.72.154.66"]   
    virtual_network_subnet_ids = [azurerm_subnet.sub_net.id]
  } 
  */
   
}

resource "azurerm_private_endpoint" "pvt_ept" {
  name                = "private-endpoint"
  location            = azurerm_resource_group.rsrc_grp.location
  resource_group_name = azurerm_resource_group.rsrc_grp.name
  subnet_id           = azurerm_subnet.sub_net.id

  private_service_connection {
    name                           = "pvt-svc_conn"
    private_connection_resource_id = azurerm_storage_account.store_acct.id
    subresource_names              = ["blob"]
    is_manual_connection           = false
  }
}