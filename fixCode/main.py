import sys
import argparse
sys.path.insert(0, '../utils')
from readConfigFile import Machine, AzureInfo

def process_command():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', '-m', required=True, help="must be either 'web', 'azfunc' or 'simulated'.")
    parser.add_argument('--path', '-p', required=True, help="must be either 'A' or 'B'.")
    return parser.parse_args()

if __name__ == '__main__':
    args = process_command()

    # ----------- get machine information -----------
    machine = Machine()
    machine.getMachineInfo('../data/client_config.txt')
    # print(machine.machineName)
    # print(machine.factory)
    # print(machine.floor)
    # print(machine.line)
    # print(machine.propertyNum)
    # print(machine.propertyName)
    # print(machine.propertyDataType)    
    # print(machine.propertyData)

    azureInfo = AzureInfo()
    azureInfo.getAzureInfo('../data/az_config.txt')
    # print(azureInfo.digital_twins_url)
    # print(azureInfo.web_url)
    # print(azureInfo.AZURE_CLIENT_ID)
    # print(azureInfo.AZURE_CLIENT_SECRET)
    # print(azureInfo.AZURE_TENANT_ID)

    if args.mode != "web" and args.mode != "simulated" and args.mode != "azfunc":
        print(f'ERROR: Wrong mode "{args.mode}". Mode should be "web", "simulated" or "azfunc".')
        sys.exit(1)
    if args.path.upper() != "A" and args.path.upper() != "B":
        print(f'ERROR: Wrong path "{args.path.upper()}". Path should be "A" or "B".')
        sys.exit(1)

    # ----------------- web code -----------------
    if args.mode == "web":
        with open('../Web/twins-init.js', "w") as output_file:
            with open('src/twins-init_sec1.txt', "r") as f:
                output_file.write(f.read())
            output_file.write(f'  {machine.machineName}: ' + '{\n' + f'    SCSFile: "{machine.machineName}",\n')
            with open('src/twins-init_sec2.txt', "r") as f:
                output_file.write(f.read())
        with open('../Web/adt.config.js', "w") as output_file:
            output_file.write('const config = {\n')
            output_file.write('  appId: ' + azureInfo.AZURE_CLIENT_ID + ",\n")
            output_file.write('  tenant: ' + azureInfo.AZURE_TENANT_ID + ",\n")
            output_file.write('  hostname: "' + azureInfo.digital_twins_url[9:] + ",\n")
            output_file.write('  password: ' + azureInfo.AZURE_CLIENT_SECRET + ",\n")
            output_file.write('};\n\nmodule.exports = config;')
        with open('../Web/src/js/adt_helper.js', "w") as output_file:
            output_file.write(f'const serverUrl = "{azureInfo.web_url[1:-1]}/";')
            with open('src/adt_helper_sec1.txt', "r") as f:
                output_file.write(f.read())
            
    # ----------------- only simulated: production_step_data.js -----------------
    elif args.mode == "simulated":
        with open('../Web/controllers/production_step_data.js', "w") as output_file:
            # ------- random_update_data -------
            with open('src/production_step_data_sec1.txt', "r") as f:
                output_file.write(f.read())
            if args.path.upper() == "A":
                output_file.write(f'    update_step_data("{machine.machineName}", vibrationAlertTriggered),\n')
            # ------- initialize_all_steps -------
            with open('src/production_step_data_sec2.txt', "r") as f:
                output_file.write(f.read())
            if args.path.upper() == "A":
                output_file.write(f'    initialize_step_data("{machine.machineName}"),\n')
            # ------- generate_data -------
            with open('src/production_step_data_sec3.txt', "r") as f:
                output_file.write(f.read())
            if args.path.upper() == "A":
                output_file.write(f'    case "{machine.machineName}":\n      data = ' + '{\n')
                for i in range(machine.propertyNum):
                    output_file.write(f'        {machine.propertyName[i]}: {machine.propertyData[i]}' + ('\n' if i == machine.propertyNum-1 else ",\n"))
                output_file.write(f'      ' + "};\n      break;\n")
            with open('src/production_step_data_sec4.txt', "r") as f:
                output_file.write(f.read())

    # ----------------- only real: index.js -----------------
    elif args.mode == "azfunc" and args.path.upper() == "B":
        with open('../AzureFunction/IoTHub2DT/index.js', "w") as output_file:
            with open('src/index_sec1.txt', "r") as f:
                output_file.write(f.read())
            output_file.write(f'    const url = {azureInfo.digital_twins_url};')
            output_file.write(f'    const digitalTwinId ="{machine.machineName}";')
            with open('src/index_sec2.txt', "r") as f:
                output_file.write(f.read())
    
    else:
        print(f'ERROR: CANNOT use mode "azfunc" with path "A" Please check again.')
        sys.exit(1)