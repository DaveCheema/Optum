provider "azurerm" {
  features {}
}

terraform {
  required_providers {    
    azurerm = {
      source = "hashicorp/azurerm"
      version= "2.50.0"
    }
    null = {
      source = "hashicorp/null"  
    }
  }
}

resource "null_resource" "pska" {
   provisioner "local-exec" {
     command = "D:\\Work Related\\Optum\\Create Azure Storage Account using CLI.ps1"
     interpreter = ["Powershell", "-File"]
  }
}