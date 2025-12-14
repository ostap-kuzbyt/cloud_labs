const { Mqtt } = require('azure-iot-device-mqtt');
const { Client, Message } = require('azure-iot-device');

class Sensor {
    constructor(connectionString) {
        this.connectionString = connectionString;
        this.client = Client.fromConnectionString(connectionString, Mqtt);
    }

    async init() { }

    generateTelemetry() {
        throw new Error("Method 'generateTelemetry' must be implemented.");
    }

    async sendTelemetry() {
        const telemetry = this.generateTelemetry();
        const data = JSON.stringify(telemetry);
        const message = new Message(data);

        message.contentType = "application/json";
        message.contentEncoding = "utf-8";

        console.log(`Sending message: ${data}`);
        await this.client.sendEvent(message);
    }
}

module.exports = Sensor;
