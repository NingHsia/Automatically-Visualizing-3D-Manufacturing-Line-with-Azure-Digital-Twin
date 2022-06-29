import sys

class Machine:
    def __init__(self):
        self.machineName = "defalutMachineName"
        self.factory = "defalutFactory"
        self.floor = "defalutFloor"
        self.line = "defalutLine"
        self.propertyNum = 0
        self.propertyName = []
        self.propertyDataType = []
        self.propertyData = []
    
    def getSimulatedData(self, dataType):
        dataType = dataType.lower()
        if dataType == "integer":
            return True, "Math.floor(Math.random() * 100)"
        elif dataType == "double":
            return True, "Math.random() * 100"
        elif dataType == "boolean":
            return True, "Math.random() > 0.9 ? true : false"
        elif dataType == "string":
            return True, "CTE7005GY4"
        else:
            return False, ""

    def getMachineInfo(self, config_file_name):
        max_property_num = 5
        max_idx = -1

        propertyNameDict = {}
        propertyTypeDict = {}
        propertyDataDict = {}
        with open(config_file_name, "r", encoding="utf8") as config_file:
            lines = config_file.readlines()
            for i, line in enumerate(lines):
                line = line.strip()
                # print(line)
                try:
                    cat, value = line.split(": ")
                    cat = cat.strip()
                    value = value.strip()
                except:
                    continue

            
                if cat == "machineName":
                    if value == "":
                        print(line)
                        print('ERROR: machineName should not be blank.')
                        sys.exit(2)
                    # if value[0].islower():
                    #     print(line)
                    #     print('ERROR: machineName should start with uppercase.')
                    #     sys.exit(2)
                    if " " in value:
                        print(line)
                        print('ERROR: There should NOT have any whitespace in machineName.')
                        sys.exit(2)
                    if value == "floor" or value == "factory" or value == "line":
                        print(line)
                        print('ERROR: Machine name should not be "factory", "flooor" or "line".')
                        sys.exit(2)
                    self.machineName = value
                elif cat == "factory":
                    if value == "":
                        print(line)
                        print('ERROR: factory should not be blank.')
                        sys.exit(2)
                    if " " in value:
                        print(line)
                        print('ERROR: There should NOT have any whitespace in factory.')
                        sys.exit(2)
                    self.factory = value
                elif cat == "floor":
                    if value == "":
                        print(line)
                        print('ERROR: floor should not be blank.')
                        sys.exit(2)
                    if " " in value:
                        print(line)
                        print('ERROR: There should NOT have any whitespace in floor.')
                        sys.exit(2)
                    self.floor = value
                elif cat == "line":
                    if value == "":
                        print(line)
                        print('ERROR: line should not be blank.')
                        sys.exit(2)
                    if " " in value:
                        print(line)
                        print('ERROR: There should NOT have any whitespace in line.')
                        sys.exit(2)
                    self.line = value
                elif "property" == cat[:8]:
                    try:
                        idx = int(cat[8:]) - 1
                    except:
                        print(line)
                        print(f'ERROR: Invalid index "{cat[8:]}".')
                        sys.exit(2)
                    if value == "":
                        print(line)
                        print(f'ERROR: {cat} should not be blank.')
                        sys.exit(2)
                    if " " in value:
                        print(line)
                        print('ERROR: There should NOT have any whitespace in property name.')
                        sys.exit(2)
                    if idx > max_idx:
                        max_idx = idx
                    propertyNameDict[idx] = value
                elif "dataType" == cat[:8]:
                    try:
                        idx = int(cat[8:]) - 1
                    except:
                        print(line)
                        print(f'ERROR: Invalid index "{cat[8:]}".')
                        sys.exit(2)
                    if value == "":
                        print(line)
                        print(f'ERROR: {cat} should not be blank.')
                        sys.exit(2)
                    if " " in value:
                        print(line)
                        print('ERROR: There should NOT have any whitespace in property data type.')
                        sys.exit(2)
                    if idx > max_idx:
                        max_idx = idx
                    
                    ret = self.getSimulatedData(value)
                    if ret[0] == True:
                        propertyTypeDict[idx] = value
                        propertyDataDict[idx] = ret[1]
                    else:
                        print(line)
                        print(f'ERROR: Invalid property data type "{value}".')
                        sys.exit(2)
                
        for i in range(max_idx+1):
            if i in propertyNameDict.keys() and i in propertyDataDict.keys():
                if self.propertyNum >= max_property_num:
                    print(f'ERROR: Too much propeties(max: 4).')
                    sys.exit(2)
                self.propertyNum += 1
                self.propertyName.append(propertyNameDict[i])
                self.propertyDataType.append(propertyTypeDict[i])
                self.propertyData.append(propertyDataDict[i])
            elif i not in propertyNameDict.keys() and i not in propertyDataDict.keys():
                continue
            else:
                print("ERROR: Property name and data type should be a pair.")
                if i in propertyNameDict.keys():
                    print(f'       Have property name {i+1}: "{propertyNameDict[i]}" but no corresponding property data type.')
                if i in propertyDataDict.keys():
                    print(f'       Have property data type {i+1}: {propertyTypeDict[i]} but no corresponding property name.')
                sys.exit(2)
        
class AzureInfo:
    def __init__(self):
        self.digital_twins_url = ""
        self.web_url = ""
        self.AZURE_CLIENT_ID = ""
        self.AZURE_CLIENT_SECRET = ""
        self.AZURE_TENANT_ID = ""

    def getAzureInfo(self, config_file_name):
        check_cnt = 0
        name_list = ["digital_twins_url", "web_url", "AZURE_CLIENT_ID", "AZURE_CLIENT_SECRET", "AZURE_TENANT_ID"]
        check_list = [False] * 5
        with open(config_file_name, "r", encoding="utf8") as config_file:
            lines = config_file.readlines()
            # print(lines)
            for i, line in enumerate(lines):
                line = line.strip()
                try:
                    cat, value = line.split(" = ")
                    cat = cat.strip()
                    value = value.strip()
                except:
                    continue
                if cat == "digital_twins_url":
                    if value == "":
                        print(line)
                        print('ERROR: Digital twins url should bde provided.')
                        sys.exit(0)
                    if " " in value:
                        print(line)
                        print('ERROR: There should NOT have any whitespace in digital twins url.')
                        sys.exit(0)
                    if value[0] != '"' or value[-1] != '"':
                        print(line)
                        print('ERROR: Digital twins url should start with " and end with ".')
                        sys.exit(0)
                    self.digital_twins_url = value
                    check_cnt += 1
                    check_list[0] = True
                elif cat == "web_url":
                    if value == "":
                        print(line)
                        print('ERROR: Web url should not be blank.')
                        sys.exit(0)
                    if " " in value:
                        print(line)
                        print('ERROR: There should NOT have any whitespace in web url.')
                        sys.exit(0)
                    if value[0] != '"' or value[-1] != '"':
                        print(line)
                        print('ERROR: Digital twins url should start with " and end with ".')
                        sys.exit(0)
                    self.web_url = value
                    check_cnt += 1
                    check_list[1] = True
                elif cat == "AZURE_CLIENT_ID":
                    if value == "":
                        print(line)
                        print('ERROR: Azure client ID should not be blank.')
                        sys.exit(0)
                    if " " in value:
                        print(line)
                        print('ERROR: There should NOT have any whitespace in Azure client ID.')
                        sys.exit(0)
                    if value[0] != '"' or value[-1] != '"':
                        print(line)
                        print('ERROR: Azure client ID should start with " and end with ".')
                        sys.exit(0)
                    self.AZURE_CLIENT_ID = value
                    check_cnt += 1
                    check_list[2] = True
                elif cat == "AZURE_CLIENT_SECRET":
                    if value == "":
                        print(line)
                        print('ERROR: Azure client secret should not be blank.')
                        sys.exit(0)
                    if " " in value:
                        print(line)
                        print('ERROR: There should NOT have any whitespace in Azure client secret.')
                        sys.exit(0)
                    if value[0] != '"' or value[-1] != '"':
                        print(line)
                        print('ERROR: Azure client secret should start with " and end with ".')
                        sys.exit(0)
                    self.AZURE_CLIENT_SECRET = value
                    check_cnt += 1
                    check_list[3] = True
                elif cat == "AZURE_TENANT_ID":
                    if value == "":
                        print(line)
                        print('ERROR: Azure tenant ID should not be blank.')
                        sys.exit(0)
                    if " " in value:
                        print(line)
                        print('ERROR: There should NOT have any whitespace in Azure tnant ID.')
                        sys.exit(0)
                    if value[0] != '"' or value[-1] != '"':
                        print(line)
                        print('ERROR: Azure tenant ID should start with " and end with ".')
                        sys.exit(0)
                    self.AZURE_TENANT_ID = value
                    check_cnt += 1
                    check_list[4] = True
        
        flag = False
        if check_cnt < 5:
            print('ERROR:', end = '')
            for i in range(5):
                if check_list[i] == False:
                    if flag == False:
                        print(' ' + name_list, end = '')
                        flag == True
                    else:
                        print(',' + name_list, end = '')
            print('needed.')
            sys.exit(0)

  