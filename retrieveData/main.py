import sys
sys.path.insert(0, '../utils')
from readConfigFile import Machine, AzureInfo
import os
import pandas as pd

def isNaN(d):
    if d == d:
        return False
    else:
        return True
def setConfig(data, machineInfo, config):
    if isNaN(data[config]): # NaN
        return 'NaN'
    if config not in machineInfo.keys():
        machineInfo[config] = data[config]
        return 'Set'
    if machineInfo[config] == data[config]:
        return 'Pass'
    else:
        return 'Conflict'

if __name__ == '__main__':
    # ----- retrieve machine info -----
    path = os.path.join('../', 'MachineInformation.xlsx')
    try:
        data = pd.read_excel(io=path, usecols=['Factory', 'Floor', 'Line', 'IoT Device Name', 'IoT Device Telemetry Data', 'Telemetry Data Type']) 
    except:
        print(f"ERROR: Can't find file 'MachineInformation.xlsx'. Please check again.")
        sys.exit(2)
    configList = ['Factory', 'Floor', 'Line', 'IoT Device Name']
    d = data
    if len(d) == 0:
        sys.exit(3)
    machineInfo = {}
    telemetryName = []
    telemetryType = []
    for i in range(len(d)):
        if isNaN(d.iloc[i]['IoT Device Telemetry Data']) and isNaN(d.iloc[i]['Telemetry Data Type']): # NaN
            continue
        elif isNaN(d.iloc[i]['IoT Device Telemetry Data']) == False and isNaN(d.iloc[i]['Telemetry Data Type']) == False: 
            telemetryName.append(d.iloc[i]['IoT Device Telemetry Data'])
            telemetryType.append(d.iloc[i]['Telemetry Data Type'])
        else:
            print(f'ERROR: Property name and data type should be a pair.')
            print(f"       Telemetry name: {d.iloc[i]['IoT Device Telemetry Data']}")
            print(f"       Telemetry type: {d.iloc[i]['Telemetry Data Type'] if isNaN(d.iloc[i]['Telemetry Data Type'])==False else ''}")
            sys.exit(2)
        for config in configList:
            ret = setConfig(d.iloc[i], machineInfo, config)
            if ret == 'Conflict':
                print(f'ERROR: {config} name conflict. Please check again.')
                sys.exit(2)
    for config in configList:
        if config not in machineInfo.keys():
            print(f'ERROR: {config} not set. Please check again')
            sys.exit(2)
    if len(telemetryName) == 0:
            print(f'ERROR: There is NO telemetry data under the device. Please check again')
            sys.exit(2)
    with open('../data/client_config.txt', "w", encoding="utf8") as config_file:  
        config_file.write('factory: ' + machineInfo['Factory'] + "\n") 
        config_file.write('floor: ' + machineInfo['Floor'] + "\n") 
        config_file.write('line: ' + machineInfo['Line'] + "\n")
        config_file.write('machineName: ' + machineInfo['IoT Device Name'] + "\n")
        for i in range(len(telemetryName)):
            config_file.write(f'property{i+1}: {telemetryName[i]}\n') 
            config_file.write(f'dataType{i+1}: {telemetryType[i]}\n') 
