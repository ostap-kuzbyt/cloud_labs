const { CosmosClient } = require("@azure/cosmos");

const COSMOS_CONNECTION_STRING = process.env.CosmosConnection;
const DATABASE_ID = "DeviceTelemetry";
const CONTAINER_ID = "DeviceTelemetry";

let client = null;
let container = null;

async function getContainer() {
    if (!container) {
        if (!COSMOS_CONNECTION_STRING) {
            throw new Error("CosmosConnection environment variable is not set.");
        }
        client = new CosmosClient(COSMOS_CONNECTION_STRING);
        const { database } = await client.databases.createIfNotExists({ id: DATABASE_ID });
        const { container: c } = await database.containers.createIfNotExists({ id: CONTAINER_ID });
        container = c;
    }
    return container;
}

async function storeTelemetry(telemetry) {
    const c = await getContainer();
    if (!telemetry.id) {
        telemetry.id = `${telemetry.DeviceId}-${Date.now()}`;
    }

    await c.items.upsert(telemetry);
    console.log(`Stored telemetry for device: ${telemetry.DeviceId}`);
}

async function getHistory(deviceId) {
    const c = await getContainer();
    const querySpec = {
        query: "SELECT * FROM c WHERE c.DeviceId = @deviceId ORDER BY c.CollectedOn DESC",
        parameters: [
            {
                name: "@deviceId",
                value: deviceId
            }
        ]
    };

    const { resources: items } = await c.items.query(querySpec).fetchAll();
    return items;
}

module.exports = {
    storeTelemetry,
    getHistory
};
