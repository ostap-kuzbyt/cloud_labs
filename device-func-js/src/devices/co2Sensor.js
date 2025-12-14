const Sensor = require('./sensor');

class Co2Sensor extends Sensor {
    constructor(connectionString) {
        super(connectionString);
        this.deviceId = "Co2Sensor";
    }

    generateTelemetry() {
        const co2 = 400 + Math.random() * 1600;
        let category = "Very Poor";
        if (co2 <= 800) category = "Good";
        else if (co2 <= 1200) category = "Moderate";
        else if (co2 <= 2000) category = "Poor";

        const lat = -90 + Math.random() * 180;
        const lon = -180 + Math.random() * 360;

        return {
            DeviceId: this.deviceId,
            Co2Level: co2,
            CollectedOn: new Date().toISOString(),
            Location: `${lat.toFixed(6)};${lon.toFixed(6)}`,
            AirQualityCategory: category,
            DeviceType: "Co2"
        };
    }
}

module.exports = Co2Sensor;
