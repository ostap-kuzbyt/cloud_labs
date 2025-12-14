const Sensor = require('./sensor');

class WeatherSensor extends Sensor {
    constructor(connectionString) {
        super(connectionString);
        this.deviceId = "WeatherSensor";
    }

    generateTelemetry() {
        const lat = -90 + Math.random() * 180;
        const lon = -180 + Math.random() * 360;

        return {
            DeviceId: this.deviceId,
            Temperature: 20 + Math.random() * 10,
            Humidity: 40 + Math.random() * 20,
            CollectedOn: new Date().toISOString(),
            Location: `${lat.toFixed(6)};${lon.toFixed(6)}`,
            DeviceType: "Weather"
        };
    }
}

module.exports = WeatherSensor;
