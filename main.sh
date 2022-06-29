# ----------- << name variables >> -----------
resourceGroupName="ResourceGroup"
dtName="DT"
webAppName="WebApp"
appRegistrationName="AppRegistration"
webAppServicePlanName="WebAppServicePlan"
functionAppName="FunctionApp"
functionName="IoTHub2DT"
functionAppHostingPlanName="FunctionAppHostingPlan"
functionAppStorageAccountName="fastorageacc"
eventSubscriptionName="EventSubscription"

CYAN='\033[0;36m'
ON_BLUE='\033[44m'
WHITE='\033[1;37m'
NOCOLOR='\033[0m'
RED='\033[0;31m'
YELLOW='\033[1;33m'

echo -e "${CYAN}######################################################################"
echo ""
echo "              Hello! Welcome to Innovation Project."
echo -e "${CYAN}"
echo -e "${CYAN}######################################################################${NOCOLOR}"
echo  "[0] Get machine information."
# --- retrieve machine info from onedrive ---
set +e
cd retrieveData
python main.py
echo "    Successfully retrieve machine information from database."
echo ""
cd ..

echo "######################################################################"
set -e
# --- login ---
echo -e "[1] ${ON_BLUE}${WIGHT}Please login your azure subscription for provisioning.${NOCOLOR}"
echo ""
az login --output none 2>/dev/null
echo "    Successfully login!"
echo ""
echo "######################################################################"
# --- choose subscription ---
echo "[2] The followings are all your subscriptions."
NumberOfSub=`az account list --query 'length([])'`
for (( j=0; j<${NumberOfSub}; j++ ))
do 
    subscriptionName=`az account list --query "[$j].name"`
    echo "      $j: $subscriptionName"
done

echo ""
j=0
subscriptionName=`az account list --query "[$j].name"`
echo -e "    ${ON_BLUE}${WIGHT}Please choose one by typing the number in front of it. For example, if you want to choose $subscriptionName, please input '0'.${NOCOLOR}"
while_loop_flag=false
while [ "$while_loop_flag" = false ]
do
    echo -n -e "    ${ON_BLUE}${WIGHT}Please input a number:${NOCOLOR} "
    read subNumber
    echo ""
    if [[ $subNumber =~ [^[:digit:]] ]]
    then
        echo -e "${RED}    ERROR: Input should be a integer. Please try again.${NOCOLOR}"
    else
        if (( $subNumber <= $NumberOfSub ))
        then
            subscriptionName=`az account list --query "[$subNumber].name"`
            subscriptionName="${subscriptionName//\"}"
            subscriptionId=`az account list --query "[$subNumber].id"`
            subscriptionId="${subscriptionId//\"}"
            az account set --subscription="${subscriptionName}"
            echo '    Successfully set subscription to "'${subscriptionName}'" (subscriptionId: '$subscriptionId').'
            while_loop_flag=true
        else
            echo -e "${RED}    ERROR: Input "'"'$subNumber'"'" out of range. Please try again.${NOCOLOR}"
        fi
    fi
done
echo ""

echo "######################################################################"
# --- choose path A/B ---
echo -e "[3] ${ON_BLUE}${WIGHT}The telemetry data should be either simulated data (path A) or real data from IoT device (path B).${NOCOLOR}"
while_loop_flag=false
while [ "$while_loop_flag" = false ]
do
    echo -n -e "    ${ON_BLUE}${WIGHT}Please input"' "A" or "B" '"to choose one data type:${NOCOLOR} "
    read path
    echo ""
    if [ "$path" = "A" ] || [ "$path" = "a" ]
    then
        echo "    Successfully choose path A: simulated data."
        while_loop_flag=true
    elif [ "$path" = "B" ] || [ "$path" = "b" ]
    then
        echo "    Successfully choose path B: real data."
        while_loop_flag=true
        echo ""

        echo "    The followings are all Azure IoT Hubs under your selected subscription."
        numOfHub=`az iot hub list --query 'length([])'`
        for (( j=0; j<${numOfHub}; j++ ))
        do 
            hubName=`az iot hub list --query "[$j].name"`
            hubRG=`az iot hub list --query "[$j].resourcegroup"`
            echo "      $j: $hubName (in resource group $hubRG)"
        done
        hubName=`az iot hub list --query "[0].name"`
        echo "    Please choose one by typing the number in front of it. For example, if you want to choose $hubName, please input '0'."
        while_loop_flag2=false
        while [ "$while_loop_flag2" = false ]
        do
            echo -n -e "    ${ON_BLUE}${WIGHT}Please input a number:${NOCOLOR} "
            read hubNumber
            echo ""
            if [[ $hubNumber =~ [^[:digit:]] ]]
            then
                echo -e "${RED}    ERROR: Input should be a integer. Please try again.${NOCOLOR}"
            else
                if (( $hubNumber <= $numOfHub ))
                then
                    iotHubName=`az iot hub list --query "[$hubNumber].name"`
                    iotHubName="${iotHubName//\"}"
                    iotHubResourceGroupName=`az iot hub list --query "[$hubNumber].resourcegroup"`
                    iotHubResourceGroupName="${iotHubResourceGroupName//\"}"
                    echo '    Successfully choose Azure Iot Hub "'${iotHubName}'" (in resource group "'$iotHubResourceGroupName'").'
                    while_loop_flag2=true
                else
                    echo -e "${RED}    ERROR: Input "'"'$hubNumber'"'" out of range. Please try again.${NOCOLOR}"
                fi
            fi
        done
    else
        echo -e "${RED}    ERROR: Invalid input "'"'$path'"'". Please try again.${NOCOLOR}"
    fi
done
echo ""

echo "######################################################################"
echo "[4] Start building Azure resources..."
prefix="automate"
echo -e "    ${ON_BLUE}${WIGHT}We will use "'"automate" as the prefix of the name of all builded resources by default. For example, the builded resource group name would be "automateResourceGroup".'"${NOCOLOR}"
while_loop_flag=false
while [ "$while_loop_flag" = false ]
do
    echo -n -e "    ${ON_BLUE}${WIGHT}Do you want to change the prefix(Y/N)?${NOCOLOR} "
    read res
    echo ""
    if [ "$res" = "Y" ] || [ "$res" = "y" ]
    then
        while_loop_flag=true
        while_loop_flag2=false
        while [ "$while_loop_flag2" = false ]
        do
            echo -n -e "    ${ON_BLUE}${WIGHT}Please input your preferred prefix (max length: 10):${NOCOLOR} "
            read prefix
            echo ""

            if [[ $prefix =~ ^[[:alnum:]-]+$ ]] 
            then
                size=${#prefix} 
                if (( $size <= 10 ))
                then
                    while_loop_flag2=true
                    echo '    Successfully change prefix to "'$prefix'".'
                    echo '    We will use "'$prefix'" as prefix in the following provisioning.'
                else
                    echo -e "${RED}    ERROR: Prefix "'"'$prefix'"'" should not be over 10 characters. Please try again."
                fi
            else
                echo -e "${RED}    ERROR: Invalid prefix "'"'$prefix'"'". Prefix can only contain letters, numbers, and dashes.. Please try again.${NOCOLOR}"
            fi
        done
    elif [ "$res" = "N" ] || [ "$res" = "n" ]
    then
        echo '    We will use "automate" as prefix in the following provisioning.'
        while_loop_flag=true
    else
        echo -e "${RED}    ERROR: Invalid input "'"'$res'"'". Please try again.${NOCOLOR}"
    fi
done
echo ""

resourceGroupName=$prefix$resourceGroupName
dtName=$prefix$dtName
webAppName=$prefix$webAppName
appRegistrationName=$prefix$appRegistrationName
webAppServicePlanName=$prefix$webAppServicePlanName
functionAppName=$prefix$functionAppName
functionAppHostingPlanName=$prefix$functionAppHostingPlanName
var=${prefix//-/}
var=${var,,}
functionAppStorageAccountName=$var$functionAppStorageAccountName
eventSubscriptionName=$prefix$eventSubscriptionName

while_loop_flag=false
while [ "$while_loop_flag" = false ]
do
    TIMESTAMP=`date +%Y-%m-%d-%H-%M-%S`
    TIMESTAMP="-"$TIMESTAMP
    echo -n -e "    ${ON_BLUE}${WIGHT}Do you want to use timestamp as suffix? For example, For example, the builded resource group name would be "'"'$resourceGroupName$TIMESTAMP'"'". (Y/N)${NOCOLOR} "
    read res
    echo ""
    if [ "$res" = "Y" ] || [ "$res" = "y" ]
    then
        while_loop_flag=true
        echo '    We will use "'$TIMESTAMP'" as suffix in the following provisioning.'
    elif [ "$res" = "N" ] || [ "$res" = "n" ]
    then
        echo "    We won't use any suffix in the following provisioning."
        while_loop_flag=true
    else
        echo -e "${RED}    ERROR: Invalid input "'"'$res'"'". Please try again.${NOCOLOR}"
    fi
done

resourceGroupName=$resourceGroupName$TIMESTAMP
dtName=$dtName$TIMESTAMP
webAppName=$webAppName$TIMESTAMP
appRegistrationName=$appRegistrationName$TIMESTAMP
webAppServicePlanName=$webAppServicePlanName$TIMESTAMP
functionAppName=$functionAppName$TIMESTAMP
functionAppHostingPlanName=$functionAppHostingPlanName$TIMESTAMP
functionAppStorageAccountName=$functionAppStorageAccountName$(($RANDOM%10))$(($RANDOM%10))
eventSubscriptionName=$eventSubscriptionName$TIMESTAMP

# --- create resource group ---
az group create --name="${resourceGroupName}" --location "East Asia" --output none
echo ""
echo '    Successfully build a resource group ''"'$resourceGroupName'".'

# --- create Azure resources using ARM template ---
# --- create dt ---
az deployment group create --name="dt" --resource-group="${resourceGroupName}" --template-file="ARMtemplate/template_dt.json" --parameters dtName="${dtName}" dtLocation="southeastasia" dtTags={} --output none
echo '    Successfully create digital twins "'$dtName'".'
# --- assign digital twins “Data Owner” role to user ---
userObjectId=$(az ad signed-in-user show --query 'objectId')
userObjectId="${userObjectId//\"}"
az dt role-assignment create --dtn="${dtName}" --assignee="${userObjectId}" --role "Azure Digital Twins Data Owner" --output none
echo '    Successfully set user to ditital twins "Data Owner" role.'
# --- create Service Principal for Web App and assign digital twins “Data Owner” role to it ---
scopeInfo=/subscriptions/$subscriptionId/resourceGroups/$resourceGroupName/providers/Microsoft.DigitalTwins/digitalTwinsInstances/$dtName
servicePrincipalId=`MSYS_NO_PATHCONV=1 az ad sp create-for-rbac --name="${appRegistrationName}" --role "Azure Digital Twins Data Owner" --scope $scopeInfo --only-show-errors`
echo '    Successfully create service principal "'$appRegistrationName'" and set it to ditital twins "Data Owner" role.'
# --- create web app ---
az deployment group create --name="webApp" --resource-group="${resourceGroupName}" --template-file="ARMtemplate/template_webApp.json" --parameters subscriptionId="${subscriptionId}" webAppName="${webAppName}" webAppLocation="East Asia" webAppHostingPlanName="${webAppServicePlanName}" webAppServerFarmResourceGroup="${resourceGroupName}" webAppAlwaysOn=false webAppCurrentStack="node" webAppPhpVersion="OFF" webAppNodeVersion="~14" webAppSku="F1" --output none
echo '    Successfully create web app "'$webAppName'".'
# --- write azure info to data/az_config.txt ---
dtUrl=`az dt show --dt-name="${dtName}" --query 'hostName'`
dtUrl="${dtUrl//\"}"
echo 'digital_twins_url = "https://'$dtUrl'"' > data/az_config.txt
webAppUrl=`az webapp show --name="${webAppName}" --resource-group="${resourceGroupName}" --query 'defaultHostName'`
webAppUrl="${webAppUrl//\"}"
echo 'web_url = "https://'$webAppUrl'"' >> data/az_config.txt
appId=`echo ${servicePrincipalId} | jq -r '.appId'`
echo 'AZURE_CLIENT_ID = "'$appId'"' >> data/az_config.txt
password=`echo ${servicePrincipalId} | jq -r '.password'`
echo 'AZURE_CLIENT_SECRET = "'$password'"' >> data/az_config.txt
tenantId=`echo ${servicePrincipalId} | jq -r '.tenant'`
echo -n 'AZURE_TENANT_ID = "'$tenantId'"' >> data/az_config.txt
echo '    Successfully record azure config.'
# --- create dtdl model, twin, relation
cd digitalTwinsInit
python digital_twin_init.py
cd ..
echo '    Successfully initialize digital twins.'

if [ "$path" = "B" ] || [ "$path" = "b" ]
then
    # --- create function app ---
    az deployment group create --name="functionApp" --resource-group="${resourceGroupName}" --template-file="ARMtemplate/template_functionApp.json" --parameters subscriptionId="${subscriptionId}" name="${functionAppName}" location="East Asia" hostingPlanName="${functionAppHostingPlanName}" serverFarmResourceGroup="${resourceGroupName}" alwaysOn=false use32BitWorkerProcess=true storageAccountName="${functionAppStorageAccountName}" netFrameworkVersion="v6.0" sku="Dynamic" skuCode="Y1" workerSize="0" workerSizeId="0" numberOfWorkers="1" --output none
    echo '    Successfully create function app "'$functionAppName'".'
    # --- set function app config ---
    az functionapp config appsettings set --name="${functionAppName}" --resource-group="${resourceGroupName}" --settings "AZURE_CLIENT_ID=$appId" --output none
    az functionapp config appsettings set --name="${functionAppName}" --resource-group="${resourceGroupName}" --settings "AZURE_CLIENT_SECRET=$password" --output none
    az functionapp config appsettings set --name="${functionAppName}" --resource-group="${resourceGroupName}" --settings "AZURE_TENANT_ID=$tenantId" --output none
    echo '    Successfully set function app "'$functionAppName'" config.'
    # --- fix azure function code (azfunc) ---
    cd fixCode
    python main.py -m azfunc -p $path
    cd ..
    echo '    Successfully fix azure function code.'
    # --- upload function code to function app ---
    cd AzureFunction
    func azure functionapp publish $functionAppName > temp.txt
    rm temp.txt
    cd ..
    echo '    Successfully create function "'$functionName'" in function app "'$functionAppName'".'
    echo -e "    ${YELLOW}Please note that since the telemetry data format from IoT Hub may differ among different devices, you may need to manually fix the data format transformation code for function app at /AzureFuction/IoTHub2DT/index.js function formatTransform() and then manually publish it to function app again, if your data format is different from our default case: Siemens S7-1500 + MOXA MC1121."
    echo -e "    For more information, please check our SOP documentation.${NOCOLOR}"


    # --- create event subscription ---
    az deployment group create --name="${eventSubscriptionName}" --resource-group="${iotHubResourceGroupName}" --template-file="ARMtemplate/template_eventSubscription.json" --parameters name="${eventSubscriptionName}" iotHubName="${iotHubName}" iotHubResourceGroupName="${iotHubResourceGroupName}" subscriptionId="${subscriptionId}" functionAppName="${functionAppName}" functionName="${functionName}" functionAppResourceGroupName="${resourceGroupName}" --output none
    echo '    Successfully create event grid subscription "'$eventSubscriptionName'" in resource group "'$iotHubResourceGroupName'".'
fi

# --- fix simulated data code (simulated) ---
cd fixCode
python main.py -m simulated -p $path
cd ..
echo '    Successfully fix simulated data code.'
# --- fix web code (web) ---
cd fixCode
python main.py -m web -p $path
cd ..
echo '    Successfully fix web code.'
# --- upload to web app ---
zipPackagePath="Web.zip"
cd Web
zip -r "../Web.zip" . > temp.txt
rm temp.txt
cd ..
az webapp config appsettings set --name="${webAppName}" --resource-group="${resourceGroupName}" --settings WEBSITE_NODE_DEFAULT_VERSION="~14" --output none
az webapp config appsettings set --name="${webAppName}" --resource-group="${resourceGroupName}" --settings SCM_DO_BUILD_DURING_DEPLOYMENT=true --output none
az webapp config appsettings set --name="${webAppName}" --resource-group="${resourceGroupName}" --settings XDT_MicrosoftApplicationInsights_NodeJS=1 --output none
az webapp config appsettings set --name="${webAppName}" --resource-group="${resourceGroupName}" --settings XDT_MicrosoftApplicationInsights_Mode=default --output none

set +e
az webapp deploy --resource-group="${resourceGroupName}" --name="${webAppName}" --src-path="${zipPackagePath}" --type zip --only-show-errors > temp.txt 2>/dev/null
if (($?))
then
    echo -e "    ${YELLOW}WARNING: An abnormal situation about input format occurs when deploying to web app.${NOCOLOR}"
fi
set -e

rm temp.txt
rm Web.zip
echo '    Successfully deploy to web app "'$webAppName'".'
echo ''
echo -e "    ${ON_BLUE}${WIGHT}Provision all done. Now you can check the result at https://$webAppUrl${NOCOLOR}"