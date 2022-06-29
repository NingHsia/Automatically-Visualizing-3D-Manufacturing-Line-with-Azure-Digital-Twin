# Automatically Visualizing 3D Manufacturing Line with Azure Digital Twins

Azure Digital Twins (ADT) is a platform that allows creating and interacting with digital representations of environments, things, people and their relationships. While 3D visualization of them allows user to navigate, understand and monitor data in Azure digital twins in an extremely simple and intuitive way.

Our toolkit is based on [Visualizing Azure Digital Twins in 3D - Microsoft Tech Community](https://techcommunity.microsoft.com/t5/internet-of-things-blog/visualizing-azure-digital-twins-in-3d/ba-p/2898159), which greatly combines Azure Digital Twins with web application to display device 3D models and their real-time telemetry data on a web page. And we use Azure CLI and ARM templates to automate the process of building and connecting all the required Azure resources such as Digital Twins, Azure function and Event Grid Subscription.

## Prerequisites
Own a Windows environment \
Own a device which is already connected to Azure IoT Hub \
Own an Azure account and a Azure subscription

## Getting Started
For more information, please check SOP Documetation.pdf.
### 1. Download software required
The following is all the software you need to install before you first run the automation code:
|  software name   | version  |
|  ----  | ----  |
| 1.	Git for Windows 64-bit  | 2.37.0 |
| 2.	Azure CLI  | 2.33.1 |
| 3.	Python  | 3.10 |
| 4.	zip and bzip2 for Git Bash on Windows  | zip: 3.0 <br> bzip2: 1.0.5|
| 5.	jq for Windows 64-bit  | 1.6 |

### 2. Run the automation code
After installing all the software required, we can run the automation code.
The following are all steps to run it:
|  step   |
|  ----  |
| 1.	Fill device information in “MachineInformation.xlsx”  |
| 2.	Put device 3D model file under specific folder  |
| 3.	Open the source code folder in Git bash  |
| 4.	Run command “bash install.sh” in Git Bash for the first time  |
| 5.	Run command “bash main.sh” in Git Bash  |

