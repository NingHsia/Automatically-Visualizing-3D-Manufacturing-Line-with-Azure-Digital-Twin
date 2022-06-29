const fetch = require('node-fetch');
const msal = require('../server/msal');
const adtConfig = require('../adt.config');

const ADT_URL = 'https://' + adtConfig.hostname + '/';

/// For randomly updating data on a schedule
/// Updading Fanning, Grinding, and Molding
function random_update_data(vibrationAlertTriggered) {
  return Promise.all([
    update_step_data("LaserWeldingRobot", vibrationAlertTriggered),
    update_step_data("CNCCutToLengthMachine", vibrationAlertTriggered),
    update_step_data("PunchMachine", vibrationAlertTriggered),
    update_step_data("SpotWeldingMachine", vibrationAlertTriggered),
    update_step_data("PaintingAndSealingSeamsMachine", vibrationAlertTriggered),
    update_step_data("MeasuringRobot", vibrationAlertTriggered),
  ]);
}

/// Randomly assign initial value to each step
function initialize_all_steps() {
  return Promise.all([
    initialize_step_data("LaserWeldingRobot"),
    initialize_step_data("CNCCutToLengthMachine"),
    initialize_step_data("PunchMachine"),
    initialize_step_data("SpotWeldingMachine"),
    initialize_step_data("PaintingAndSealingSeamsMachine"),
    initialize_step_data("MeasuringRobot"),
  ]);
}

async function update_step_data(deviceType, vibrationAlertTriggered) {
  let token = await msal.getToken();

  const url = ADT_URL + 'digitaltwins/' + deviceType + '?api-version=2020-10-31';
  const data = generate_data(deviceType, vibrationAlertTriggered);
  var mapped_data = [];
  for (const [key, value] of Object.entries(data)) {
    mapped_data.push({
      op: "replace",
      path: "/" + key,
      value: value
    });
  }

  return await fetch(url, {
    method: 'PATCH', headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + token
    },
    body: JSON.stringify(mapped_data)
  });

}

// deviceType: "grinding", "fanning", "conching", "winnowing", or "molding"
async function initialize_step_data(deviceType) {
  let token = await msal.getToken();

  const url = ADT_URL + 'digitaltwins/' + deviceType + '?api-version=2020-10-31';
  const data = generate_data(deviceType, false);
  var mapped_data = [];
  for (const [key, value] of Object.entries(data)) {
    mapped_data.push({
      op: "add",
      path: "/" + key,
      value: value
    });
  }

  return await fetch(url, {
    method: 'PATCH', headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + token
    },
    body: JSON.stringify(mapped_data)
  });

}

// Generating message for "grinding", "fanning", or "molding"
// Return a string
function generate_data(deviceType, vibrationAlertTriggered) {
  var data = {};
  switch (deviceType) {
    case "LaserWeldingRobot":
      data = {
        temperature: Math.random() * 100,
        distance: Math.random() * 100
      };
      break;
    case "CNCCutToLengthMachine":
      data = {
        Temperature: 30 + Math.random() * 20, // range: [30, 50]
        Pressure: 400 + Math.random() * 200 // range: [400, 600]
      };
      break;
    case "PunchMachine":
      data = {
        Temperature: 500 + Math.random() * 200, // range: [500, 700]
        MagneticField: 300 + Math.random() * 200, // range: [300, 500]
        Pressure: 400 + Math.random() * 200 // range: [400, 600]
      };
      break;
    case "SpotWeldingMachine":
      data = {
        Distance: 20 + Math.floor(Math.random() * 40) // range: [20, 60]
      };
      break;
    case "PaintingAndSealingSeamsMachine":
    case "MeasuringRobot":
      data = {
        Torque: 20000 + Math.random() * 10000 // range: [20000, 30000]
      };
  }

  return data;
}

// Utility Function
function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

module.exports = {
  random_update_data,
  initialize_all_steps
};