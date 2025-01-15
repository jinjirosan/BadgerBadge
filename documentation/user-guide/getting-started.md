# Getting Started with BadgerBadge

This guide will help you get started with your BadgerBadge device, whether it's the Eva or Papa variant.

## Initial Setup

1. **Hardware Check**
   - Verify battery connection
   - Check BME680 sensor connection
   - Ensure SigFox module is connected
   - Confirm display functionality

2. **Power On**
   - Press any button to wake the device
   - Wait for initial boot sequence
   - Check battery indicator

## Basic Navigation

1. **Main Menu**
   - Use A and C buttons to navigate pages
   - Press button under app icon to launch
   - Press A+C together to return to menu
   - Check battery status in top-right

2. **App Navigation**
   - Each app uses consistent controls:
     - Button A: Previous/Left
     - Button B: Select/Action
     - Button C: Next/Right
     - A+C together: Exit to menu

## Configuration Files

1. **Personal Information**
   - Edit `badge.txt` for badge details
   - Update `medical.txt` for medical info
   - Configure `help.txt` for emergency contacts
   - Modify `checklist.txt` for list items

2. **App Settings**
   - `focus.txt` for focus timer presets
   - `timer.txt` for activity timers
   - `comms.txt` for communication settings

## First-Time Setup

1. **Badge Configuration**
   ```
   1. Prepare your badge image (296x128 px)
   2. Convert to binary format
   3. Place in root directory
   4. Update badge text information
   ```

2. **Emergency Information**
   ```
   1. Update medical information
   2. Add emergency contacts
   3. Configure SigFox messaging
   4. Test emergency features
   ```

3. **Daily Use Setup**
   ```
   1. Customize checklist items
   2. Set up timer activities
   3. Configure focus periods
   4. Add personal photos
   ```

## Basic Features

### Core Apps
- **Badge**: Personal identification
- **List**: Daily item checklist
- **Image**: Photo gallery

### Utility Apps
- **Timer**: Activity timing
- **Temperature**: Environmental monitoring
- **Elevation**: Height tracking

### Focus App
- **Focus**: Concentration timer

### Emergency Apps
- **Medical**: Health information
- **Help/SOS**: Emergency contacts
- **Communications**: SigFox messaging

## Maintenance

1. **Battery Care**
   - Check battery level regularly
   - Charge when below 20%
   - Use provided charging circuit
   - Monitor charging LED

2. **Display Care**
   - Clean with soft cloth
   - Avoid screen pressure
   - Use screen refresh when needed
   - Prevent direct sunlight exposure

3. **System Updates**
   - Keep configuration files current
   - Update emergency contacts
   - Refresh medical information
   - Maintain checklist items

## Troubleshooting

1. **Display Issues**
   - Press any button to wake
   - Check battery level
   - Try system refresh (A+B+C)
   - Verify contrast settings

2. **Sensor Problems**
   - Check I2C connections
   - Verify sensor readings
   - Calibrate if necessary
   - Monitor error messages

3. **Communication Issues**
   - Check SigFox signal
   - Verify message format
   - Test transmission
   - Monitor LED indicators

## Support

For additional help:
- Check documentation
- Review error logs
- Contact support team
- Visit project repository

## Next Steps

1. **Customize Your Badge**
   - Add personal images
   - Update contact info
   - Set up daily routines
   - Configure emergency data

2. **Regular Use**
   - Monitor battery level
   - Update information regularly
   - Back up configuration files
   - Test emergency features

3. **Advanced Features**
   - Explore SigFox capabilities
   - Use environmental monitoring
   - Track elevation changes
   - Optimize focus sessions 