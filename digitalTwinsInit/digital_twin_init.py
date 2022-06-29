from azure.identity import ClientSecretCredential
from azure.digitaltwins.core import DigitalTwinsClient
from utils import create_original_models, create_new_model, create_static_relations, create_production_line_relations, filter_twin_model, modelId2TwinId
import sys
sys.path.insert(0, '../utils')
from readConfigFile import Machine, AzureInfo

## init variables
azureInfo = AzureInfo()
azureInfo.getAzureInfo('../data/az_config.txt')
## remove "" using [1:-1]
credential = ClientSecretCredential(azureInfo.AZURE_TENANT_ID[1:-1], azureInfo.AZURE_CLIENT_ID[1:-1], azureInfo.AZURE_CLIENT_SECRET[1:-1])
service_client = DigitalTwinsClient(azureInfo.digital_twins_url[1:-1], credential)

machine = Machine()
machine.getMachineInfo('../data/client_config.txt')
twinId = machine.machineName
original_model_folder_path = "./digital_twin_models/"
sample_production_twins = ["CNCCutToLengthMachine", "PunchMachine", "SpotWeldingMachine", "PaintingAndSealingSeamsMachine", "MeasuringRobot"] 

## create model and upload
# print('Created Models:')
new_machine_model = create_new_model(twinId, machine.propertyName, machine.propertyDataType)
all_models = create_original_models(original_model_folder_path)
all_models.append(new_machine_model)

models = service_client.create_models(all_models)

## create twins
all_twins = []
print('    Created Digital Twin: ', end="")
first_flag = True
for model in filter_twin_model(all_models):
    digital_twin_id = modelId2TwinId(model["@id"], machine)
    temporary_twin = {
        "$metadata": {
            "$model": model["@id"]
        },
        "$dtId": digital_twin_id,
    }
    all_twins.append(temporary_twin)
    created_twin = service_client.upsert_digital_twin(digital_twin_id, temporary_twin)
    if first_flag == True:
        print(created_twin["$dtId"], end="")
        first_flag = False
    else:
        print(f', {created_twin["$dtId"]}', end="")
print("")
## create relationships
relationships = create_static_relations(machine)
# relationships += create_production_line_relations(sample_production_twins + [twinId.capitalize()])
relationships += create_production_line_relations(sample_production_twins + [twinId], machine)

for relationship in relationships:
    service_client.upsert_relationship(
        relationship["$sourceId"],
        relationship["$relationshipId"],
        relationship
    )

