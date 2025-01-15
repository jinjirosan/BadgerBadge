# Utility Applications

The utility applications provide environmental monitoring and measurement capabilities using the BME680 sensor and other hardware features.

## Available Apps

### [Temperature App](temperature.md)
Environmental monitoring featuring:
- Temperature readings
- Humidity measurement
- Pressure tracking
- Air quality assessment

### [Elevation App](elevation.md)
Height and floor tracking with:
- Altitude measurement
- Floor level calculation
- Ground calibration
- Pressure-based tracking

## Common Features

All utility apps share:
- BME680 sensor integration
- Real-time monitoring
- Calibration capabilities
- State management
- Error handling

## Sensor Integration

### Hardware Details
- BME680 environmental sensor
- I2C interface
- Pins: SDA (4), SCL (5)
- Fast update mode

### Measurements
- Temperature (-40°C to 85°C)
- Humidity (0-100%)
- Pressure (300-1100 hPa)
- Gas resistance

## Configuration

Shared configuration parameters:
- Temperature offset: -1.5°C
- Sea level pressure: 1013.25-1015.5 hPa
- Update frequency
- Display preferences

## Usage

See individual app documentation for detailed usage instructions:
- [Temperature App Documentation](temperature.md)
- [Elevation App Documentation](elevation.md) 