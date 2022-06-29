from statistics import mode
from azure.identity import ClientSecretCredential
from azure.digitaltwins.core import DigitalTwinsClient
import sys
sys.path.insert(0, '../utils')
from readConfigFile import Machine, AzureInfo

azureInfo = AzureInfo()
azureInfo.getAzureInfo('../data/az_config.txt')
credential = ClientSecretCredential(azureInfo.AZURE_TENANT_ID[1:-1], azureInfo.AZURE_CLIENT_ID[1:-1], azureInfo.AZURE_CLIENT_SECRET[1:-1])
service_client = DigitalTwinsClient(azureInfo.digital_twins_url[1:-1], credential)

query_expression = 'SELECT * FROM digitaltwins'

print('DigitalTwins Cleaning ... ')

query_result = service_client.query_twins(query_expression)
while query_result:
    temp = []
    for twin in query_result:
        try:
            relationships = service_client.list_relationships(twin["$dtId"])
            for relationship in relationships:
                service_client.delete_relationship(twin["$dtId"], relationship["$relationshipId"])
            service_client.delete_digital_twin(twin["$dtId"])
        except:
            temp.append(twin)
    if temp:
        query_result = temp
    else:
        break

listed_models = service_client.list_models()
while listed_models:
    temp = []
    for model in listed_models:
        try:
            service_client.delete_model(model.id)
        except:
            temp.append(model)
    if temp:
        listed_models = temp
    else:
        break
    

print('Finish DigitalTwins Cleaning.')

    
    