const { app } = require('@azure/functions');
const WeatherSensor = require('../devices/weatherSensor');
const Co2Sensor = require('../devices/co2Sensor');

const WEATHER_CONN_STRING = process.env.WEATHER_DEVICE_CONNECTION_STRING;
const CO2_CONN_STRING = process.env.CO2_DEVICE_CONNECTION_STRING;
const DELAY_MS = parseInt(process.env.DELAY_MS || "1000");
const MAX_REQUESTS = parseInt(process.env.MAX_REQUESTS || "100");

app.http('fakeLoad', {
    methods: ['POST', 'GET'],
    authLevel: 'function',
    handler: async (request, context) => {
        context.log('FakeLoad function triggered.');

        if (!WEATHER_CONN_STRING || !CO2_CONN_STRING) {
            return {
                status: 500,
                body: "Connection strings not configured."
            };
        }

        const weatherSensor = new WeatherSensor(WEATHER_CONN_STRING);
        const co2Sensor = new Co2Sensor(CO2_CONN_STRING);

        let requests = 0;
        context.log(`Starting simulation. Delay: ${DELAY_MS}ms, Max Requests: ${MAX_REQUESTS}`);

        while (requests < MAX_REQUESTS) {
            try {
                await weatherSensor.sendTelemetry();
                await co2Sensor.sendTelemetry();
                requests += 2;
                context.log(`Sent request batch ${requests}`);
            } catch (err) {
                context.log.error("Error sending telemetry:", err);
            }

            await new Promise(resolve => setTimeout(resolve, DELAY_MS));
        }

        return {
            status: 200,
            body: "Fake load executed."
        };
    }
});
