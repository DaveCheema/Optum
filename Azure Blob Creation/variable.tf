#Create variable.tf
variable "prefix" {
  type    = string
  default = "dc1"
}
variable "resource_group_name" {
  type    = string
  default = "dc1-rg"
}
variable "storage_acct_name" {
  type    = string
  default = "dc1storacct1"
}
variable "location" {
  type    = string
  default = "westus"
}
variable "domain_name" {
  type    = string
  default = "davescheemagmail.onmicrosoft.com"
}

variable "subscription" {
  type    = string
  default = "dee29fa2-d695-439c-80a5-158ce469882b"
}
variable "vnet_name" {
  type    = string
  default = "dc1-vnet1"
}
variable "subnet_name" {
  type    = string
  default = "default"
}
variable "subnet2_name" {
  type    = string
  default = "sub-net2"
}
variable "adddr_prefix" {
  type    = string
  default = "10.0.0.0/16"
}
variable "subnet_addr_prefix" {
  type    = string
  default = "10.0.1.0/24"
}
variable "subnet-2-addr_prefix" {
  type = string
  default = "10.0.2.0/24"  
}

variable "account_tier" {
  type    = string
  default = "Standard"
}
variable "container1_name" {
  type    = string
  default = "input"
}

variable "enable_blob_encryption" {
  type    = string
  default = "true"

}

variable "access_tier" {
  type    = string
  default = "Hot"
}

variable "account_kind" {
  type    = string
  default = "StorageV2"
}
variable "allow_blob_public_access" {
  type    = string
  default = "false"
}
variable "account_replication_type" {
  type    = string
  default = "RAGRS"
}
variable "container_access_type" {
  type    = string
  default = "private" #"container" # "blob" #"private"
}
variable "private_endpoint_name" {
  type    = string
  default = "dc1pvtendpoint1"
}
variable "delete_retention_days" {
  type    = number
  default = 7
}
variable "min_tls_version" {
  type    = string
  default = "TLS1_2"
}

variable "tags" {
  type = map(any)
  default = {
    Environment = "non-prod"
    Team        = "Loki"
  }
}