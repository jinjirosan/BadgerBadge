# Hardware Specifications

## Core Platform

- **Main Platform**: Pimoroni Badger2040
- **Display**: E-ink display
- **Hardware Version**: Platform v3.0

## Power System

- **Battery**: 150 mAh LiPo
- **Charging Circuit**: LiPo Amigo
- **Operating Voltage**:
  - Maximum: 4.0V
  - Minimum: 3.15V
- **Power Management**: Built-in sleep/wake system

## Sensors

### Environmental Sensor
- **Model**: BME680
- **Measurements**:
  - Temperature
  - Humidity
  - Pressure
  - Gas

### Communications
- **Module**: LPWAN SigFox Node
- **Frequency**: 868MHz
- **Antenna**: uFL 850MHz flat sticker antenna
- **Message Capacity**: 140 12-byte daily messages
- **Coverage**: Europe-wide positioning

## Input/Output

### Display
- **Type**: E-ink
- **Resolution**: Badger2040 native resolution
- **Update Modes**: 
  - Fast update
  - Full refresh

### Buttons
- 3 Physical buttons (A, B, C)
- Multi-function capabilities
- Wake-from-sleep support

### LED
- Status LED
- Programmable brightness

## Interfaces

### Serial
- UART (TX: Pin 0, RX: Pin 1)
- Baud Rate: 9600

### I2C
- Used for BME680 sensor
- Built-in bus scanning capability

## Storage

- Internal storage for:
  - Application states
  - Configuration files
  - Image data
  - User settings

## Physical Specifications

- Compact form factor
- Optimized for wearability
- Child-friendly design
- Durable construction

## Power Consumption

- Sleep mode for power saving
- Efficient e-ink display
- Battery monitoring system
- Low-power sensor operation 