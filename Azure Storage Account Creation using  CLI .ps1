#Define environment variables.
$prefix = "dc1"
$storage_acct_name = "${prefix}storacct1";
$resource_group = "${prefix}-rg";
$location = "westus";
$domain_name = "davescheemagmail.onmicrosoft.com";
$subscription = "dee29fa2-d695-439c-80a5-158ce469882b";
$environment = "non-prod";
$vnet_name = "${prefix}-vnet1";
$subnet_name = "default";
$adddr_prefix = "10.2.0.0/16";
$subnet_addr_prefix = "10.2.0.0/24";
$storage_lock_name = "${prefix}_delete_lock";
$resource_group = "${prefix}-rg"
$access_tier = "Hot";
$allow_blob_public_access = "false";
$sku = "Standard_RAGRS";
$private_endpoint_name = "${prefix}pvtendpoint1";
$delete_retention_days = 7;

#Create resource group, if it does not exist.
if ($null -eq ${az group exists `
	--name $resource_group `
    --subscription $subscription})
{
	az group create `
	--location $location `
    --name $resource_group `
    --subscription $subscription `
    --tags environment=$environment;
	
}else {
   write-host("${resource_group} already exists")
}
	
#Create vnet and subnet
if ($null -eq 
	${az network vnet show `
		--name $vnet_name `
		--resource-group dc1-rg `
		--query name `
		--output tsv})
{
	az network vnet create `
		--address-prefixes $adddr_prefix `
		--name $vnet_name `
		--resource-group $resource_group `
		--location $location `
		--subnet-name $subnet_name `
		--subnet-prefixes $subnet_addr_prefix `
		--subscription $subscription `
		--tags environment=$environment;
		
	#Update vnet subnet to enable private endpoint.
	az network vnet subnet update `
		--name $subnet_name `
		--resource-group $resource_group `
		--vnet-name $vnet_name `
		--disable-private-endpoint-network-policies true `
		--disable-private-link-service-network-policies true;
}else{
	write-host("${vnet_name} and ${subnet_name} already exist.")
}
	
#Create storage account
if ($null -eq 
	${az storage account show `
		 --ids /subscriptions/$subscription/resourceGroups/$resource_group/providers/Microsoft.Storage/storageAccounts/$storage_acct_name `
		 --query name --output tsv})
{
	az storage account create `
		 --name $storage_acct_name `
		 --resource-group $resource_group `
		 --access-tier $access_tier `
		 --allow-blob-public-access $allow_blob_public_access `
		 --assign-identity `
		 --bypass "None" `
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
	
	#Get storage account ID.
	$storage_account_id=$(az storage account list `
		--resource-group $resource_group `
		--query '[].[id]' `
		--output tsv);
}else{
	write-host("${storage_acct_name} already exists")
}

#Create private endpoint.
if ($null -eq 
	${az network private-endpoint show `
		 --ids /subscriptions/$subscription/resourceGroups/$resource_group/providers/Microsoft.Network/privateLinkServices/$private_endpoint_name `
		 --query name --output tsv})
{
	#Create private endpoint.
	az network private-endpoint create `
		--name $private_endpoint_name `
		--resource-group $resource_group `
		--vnet-name $vnet_name --subnet $subnet_name `
		--private-connection-resource-id $storage_account_id `
		--group-id blob `
		--connection-name ${prefix}Connection;
}else{
	write-host("${private_endpoint_name} already exists")
}
	
#Create storage lock to prevent accidental delete
if ($null -eq 
	${az resource lock show `
		--name $storage_lock_name `
		--resource-group $resource_group `
		--resource $storage_acct_name `
		--resource-type Microsoft.Storage/storageAccounts})
{
	#Create storage lock to prevent accidental delete
	az resource lock create `
		--lock-type CanNotDelete `
		--name $storage_lock_name `
		--resource $storage_acct_name `
		--resource-group $resource_group `
		--resource-type Microsoft.Storage/storageAccounts `
		--subscription $subscription; 
}else{
	write-host("${storage_lock_name} already exists")
}

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