const { app } = require('@azure/functions');
const cosmosService = require('../services/cosmosService');

app.eventHub('hubListener', {
    connection: 'HubConnection',
    eventHubName: 'sensor-hub',
    cardinality: 'many',
    consumerGroup: '$Default',
    handler: async (messages, context) => {
        context.log("HubListener triggered! Messages received:", messages.length);
        context.log(`Event Hub trigger function processed ${messages.length} messages`);

        for (const message of messages) {
            try {
                let telemetry = message;
                if (typeof message === 'string') {
                    try {
                        telemetry = JSON.parse(message);
                    } catch (e) {
                        context.log.error("Failed to parse message string:", message);
                        continue;
                    }
                } else if (Buffer.isBuffer(message)) {
                    try {
                        telemetry = JSON.parse(message.toString());
                    } catch (e) {
                        context.log.error("Failed to parse message buffer");
                        continue;
                    }
                }
                if (!telemetry || !telemetry.DeviceId) {
                    context.log.warn("Received invalid telemetry:", telemetry);
                    continue;
                }

                await cosmosService.storeTelemetry(telemetry);
            } catch (err) {
                context.log.error("Error processing message:", err);
            }
        }
    }
});
