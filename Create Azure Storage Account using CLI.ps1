#Define environment variables.
$storage_acct_name = "dc1storacct1";
$resource_group = "dc1-rg";
$location = "westus";
$domain_name = "davescheemagmail.onmicrosoft.com";
$subscription = "dee29fa2-d695-439c-80a5-158ce469882b";
$environment = "non-prod";
$vnet_name = "dc1-vnet1";
$subnet_name = "default";
$adddr_prefix = "10.2.0.0/16";
$subnet_addr_prefix = "10.2.0.0/24";
$access_tier = "Hot";
$allow_blob_public_access = "false";
$sku = "Standard_RAGRS";
$private_endpoint_name = "dc1pvtendpoint1";
$delete_retention_days = 7;

#Create resource group
az group create `
	--location $location `
    --name $resource_group `
    --subscription $subscription `
    --tags environment=$environment;
	
#Create vnet and subnet
az network vnet create `
	--address-prefixes $adddr_prefix `
	--name $vnet_name `
	--resource-group $resource_group `
	--location $location `
	--subnet-name $subnet_name `
	--subnet-prefixes $subnet_addr_prefix `
	--subscription $subscription `
	--tags environment=$environment;
	
#Create storage account
az storage account create `
	 --name $storage_acct_name `
	 --resource-group $resource_group `
	 --access-tier $access_tier `
	 --allow-blob-public-access $allow_blob_public_access `
	 --assign-identity `
	 --bypass None `
	 --default-action Deny  `
	 --domain-name $domain_name `
	 --enable-hierarchical-namespace false `
	 --encryption-services blob `
	 --https-only true `
	 --kind StorageV2 `
	 --location $location `
	 --min-tls-version TLS1_2 `
	 --publish-internet-endpoints false `
	 --publish-microsoft-endpoints true `
	 --require-infrastructure-encryption false `
	 --routing-choice MicrosoftRouting `
	 --sku $sku `
	 --subscription $subscription `
	 --tags environment=$environment;
	 
#Update vnet subnet to enable private endpoint.
az network vnet subnet update `
    --name $subnet_name `
    --resource-group $resource_group `
    --vnet-name $vnet_name `
	--disable-private-endpoint-network-policies true `
    --disable-private-link-service-network-policies true;
	
#Get storage account ID.
$storage_account_id=$(az storage account list `
	--resource-group $resource_group `
	--query '[].[id]' `
	--output tsv);
	
#Create private endpoint.
az network private-endpoint create `
    --name $private_endpoint_name `
    --resource-group $resource_group `
    --vnet-name $vnet_name --subnet $subnet_name `
    --private-connection-resource-id $storage_account_id `
    --group-id blob `
    --connection-name dc1Connection;
	
#Create storage lock to prevent accidental delete
az resource lock create `
	--lock-type CanNotDelete `
	--name delete_lock `
	--resource $storage_acct_name `
	--resource-group $resource_group `
	--resource-type Microsoft.Storage/storageAccounts `
	--subscription $subscription; 

#Get storage account id.
$storage_account_id=$(az resource show `
    --name $storage_acct_name `
    --resource-group $resource_group `
    --resource-type Microsoft.Storage/storageAccounts `
    --query id `
    --output tsv);

#Prevent user from using Shared Access Key.
az resource update `
	--ids $storage_account_id `
	--set properties.allowSharedKeyAccess=false;
	
#Allow trusted Microsoft services to access this storage account 
az storage account update `
	--resource-group $resource_group `
	--name $storage_acct_name `
	--bypass "AzureServices";

#Turn on blob change feed.
az storage account blob-service-properties update `
	--enable-change-feed true `
	--enable-delete-retention true `
	--delete-retention-days $delete_retention_days `
	--account-name $storage_acct_name `
	--resource-group $resource_group;

#Turn on the Azure Defender for storage.
az security pricing create `
	--name StorageAccounts `
	--tier "standard" `
	--subscription $subscription;