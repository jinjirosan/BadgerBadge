# Elevation App Documentation

The Elevation app uses the BME680 sensor to measure and display altitude changes, floor levels, and atmospheric conditions. It provides real-time elevation tracking with ground-level calibration.

## Features

- Altitude measurement
- Floor level calculation
- Temperature monitoring
- Pressure tracking
- Ground level calibration
- Real-time updates

## Interface

### Display Elements
- Current altitude
- Floor level
- Temperature
- Pressure reading
- Reference values
- Battery status

### Controls
- **Button A**: Calibrate ground level
- **Button B**: Toggle display mode
- **Button C**: Refresh readings
- **A + C**: Exit to main menu

## Sensor Integration

### Hardware
- **Sensor**: BME680
- **Interface**: I2C
- **Pins**:
  - SCL: Pin 5
  - SDA: Pin 4
- **Update Speed**: Fast mode

## Configuration

### Environmental Parameters
- Temperature offset: -1.5°C
- Sea level pressure: 1015.5 hPa (Netherlands average)
- Ground level calibration
- Local pressure reference

## Features

### Altitude Measurement
- Real-time altitude tracking
- Ground level calibration
- Relative height calculation
- Metric display (meters)

### Floor Calculation
- Standard floor height
- Ground floor reference
- Automatic calculation
- Dynamic updates

### Environmental Monitoring
- Temperature compensation
- Pressure normalization
- Altitude correction
- Trend tracking

## Calculations

### Altitude Determination
1. **Pressure-Based**:
   - Atmospheric pressure reading
   - Temperature compensation
   - Sea level reference
   - Altitude calculation

2. **Floor Level**:
   - Height above ground
   - Standard floor height
   - Rounding algorithm
   - Display conversion

### Sensor Readings
- Temperature (°C)
- Pressure (hPa)
- Relative altitude (m)
- Floor number

## Technical Details

### Sensor Configuration
- Fast update mode
- Temperature compensation
- Pressure calibration
- Altitude calculation

### Data Processing
- Rolling averages
- Noise filtering
- Height calculation
- Floor determination

### Display Updates
- Real-time readings
- Clear formatting
- Unit conversion
- Status indicators

## Error Handling

- Sensor verification
- Reading validation
- Range checking
- Error display
- Recovery procedures

## State Management

### Calibration Data
- Ground level pressure
- Temperature reference
- Altitude offset
- System state

### Update Frequency
- Continuous monitoring
- Display refresh
- State saving
- Calibration checks

## Customization

### Calibration
1. Set ground level
2. Adjust temperature offset
3. Configure sea level pressure
4. Set floor height

### Display Options
- Altitude units
- Floor display
- Update frequency
- Information detail

## Performance

### Power Management
- Efficient polling
- Display optimization
- Sleep mode support
- Battery monitoring

### Memory Usage
- Minimal state storage
- Efficient calculations
- Resource management
- Clean operation

## Integration

### Height Tracking
- Continuous monitoring
- Relative changes
- Floor transitions
- Status updates

### System Interface
- I2C communication
- State management
- Display control
- Power handling

## Usage Instructions

1. **Initial Setup**:
   - Launch application
   - Wait for sensor stabilization
   - Calibrate ground level
   - Begin monitoring

2. **Ground Calibration**:
   - Stand at ground level
   - Press A to calibrate
   - Wait for confirmation
   - Start measurements

3. **Floor Tracking**:
   - Move between floors
   - Watch automatic updates
   - Check floor number
   - Monitor changes

4. **Environmental Data**:
   - View temperature
   - Check pressure
   - Monitor trends
   - Track changes 