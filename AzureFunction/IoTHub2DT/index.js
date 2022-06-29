const { DefaultAzureCredential } = require("@azure/identity");
const { DigitalTwinsClient } = require("@azure/digital-twins-core");
const  jwt_decode  = require('jwt-decode');

function formatTransform(eventGridEvent) {
    /*  According to your data format from IoT Hub, your data selector will differ.
        No matter what your data selector is, you should transform your data to match the below required data format: 
            var data = [
                {
                    "DisplayName": "Your_Display_Name", 
                    "Value": "Teletry_Data_Value"
                }, 
                {
                    "DisplayName": "Your_Display_Name", 
                    "Value": "Teletry_Data_Value"
                },
                ...
            ] 

        Our default case: OPC UA Server Data Selector (Siemens S7-1500 + MOXA MC1121) data format to required data format
        Please fix this transformation function if needed. 
    */
   
    // Modbus Data Selector to required data format
    // var decodedHeader = jwt_decode(eventGridEvent.data.body, { header: true });
    // var data = decodedHeader.Content[0].Data[0].Values

    var data =[]
    eventGridEvent.data.body.forEach(element => {
        data.push({
            "DisplayName":element.NodeId.split('.')[element.NodeId.split('.').length - 1],
            "Value": element.Value.Value
        })
    })
    return data
}

module.exports = async function (context, eventGridEvent) {

    context.log("Subject: " + eventGridEvent.subject);
    // context.log("subject type"+ typeof(eventGridEvent.subject))
    // decode jwt token
    // context.log(eventGridEvent.data)
    // context.log(eventGridEvent.data.body)

    var data = formatTransform(eventGridEvent)    
    const url = "https://videoDT-2022-05-30-10-23-18.api.sea.digitaltwins.azure.net";    
    const digitalTwinId ="LaserWeldingRobot";    
    const credential = new DefaultAzureCredential();
    const serviceClient = new DigitalTwinsClient(url, credential);

    var patch = []
    data.forEach(element => {  
        patch.push({
            "op": "add",
            "path": "/" + element.DisplayName,
            "value": element.Value
        })
    });

    context.log('patched data: ' + JSON.stringify(patch))
    const updatedTwin = await serviceClient.updateDigitalTwin(digitalTwinId, patch);
    context.log(updatedTwin)
    context.log('Successfully update twin using Digital Twins SDK!')
};