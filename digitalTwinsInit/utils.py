
import os
import json

from pkg_resources import register_namespace_handler
def create_original_models(path):
    all_files = os.listdir(path)
    all_models = []
    for file in all_files:
        if ".json" in file:
            with open(path + file) as f:
                obj = json.loads(f.read())
            all_models.append(obj)
    return all_models

##　create new model
def create_new_model(twinId, propertyName, propertyDataType):
    new_machine_model = {
    "@id": "dtmi:com:microsoft:iot:e2e:digital_factory:production_step_{};1".format(twinId),
    "@type": "Interface",
    "displayName": "Factory Production Step: {} - Interface Model".format(twinId),
    "extends": "dtmi:com:microsoft:iot:e2e:digital_factory:production_step;1",
    "@context": "dtmi:dtdl:context;2",
    "contents": []
    }
    for n, t in zip(propertyName, propertyDataType):
        new_machine_model["contents"].append( {
            "@type": "Property",
            "name": n,
            "schema": t
        },)  
    return new_machine_model

def create_static_relations(machine):
    relationships = [
    {
        "$relationshipId": "factory_2_floor",
        "$sourceId": machine.factory,
        "$relationshipName": "rel_has_floors",
        "$targetId": machine.floor,
    },
     {
        "$relationshipId": "floor_2_production",
        "$sourceId": machine.floor,
        "$relationshipName": "rel_runs_lines",
        "$targetId": machine.line,
    }]
    return relationships
def create_production_line_relations(twinIds, machine):
    relations = []
    for twinId in twinIds:
        relations.append(
             {
                "$relationshipId": "production_2_{}".format(twinId),
                "$sourceId": machine.line,
                "$relationshipName": "rel_runs_steps",
                "$targetId": twinId,
            }
        )
    return relations
def filter_twin_model(models):
    interface_extend_model = ["dtmi:com:microsoft:iot:e2e:digital_factory:model_metadata;1", "dtmi:com:microsoft:iot:e2e:digital_factory:production_step;1"]
    return [m for m in models if m["@id"] not in interface_extend_model]

def modelId2TwinId(name, machine):
    # return name.split(":")[-1].split(";")[0].split("_")[-1].capitalize() 
    ret_name = name.split(":")[-1].split(";")[0].split("_")[-1]
    # ret_name = ret_name[0].upper() + ret_name[1:]
    if ret_name == "factory":
        ret_name = machine.factory
    elif ret_name == "floor":
        ret_name = machine.floor
    elif ret_name == "line":
        ret_name = machine.line
    return ret_name