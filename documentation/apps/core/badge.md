# Badge App Documentation

The Badge app serves as a digital identification card, displaying personal information, contact details, and optionally a QR code. It's designed to be both informative and visually appealing on the e-ink display.

## Features

- Personal identification display
- Switchable badge/QR code views
- SigFox communication capability
- Battery status monitoring
- LED status indication
- Image display support

## Interface

### Display Elements
- Personal photo/image
- Name and details
- Company/Organization
- Contact information
- Battery status
- QR code (optional view)

### Display Layout
- Image Width: 104 pixels
- Company Height: 30 pixels
- Details Height: 20 pixels
- Name section uses remaining space
- Left padding: 5 pixels

### Controls
- **Button A**: Toggle QR code view
- **Button B**: Toggle LED/Send SigFox
- **Button C**: Switch views
- **A + C**: Exit to main menu

## Configuration

The app uses several configuration files:
- `badge-image.bin`: Main badge image
- `badge-image_QR.bin`: QR code version
- Text configuration in code

### Default Text Format
\`\`\`
mustelid inc
H. Badger
RP2040
2MB Flash
E ink
296x128px
\`\`\`

## Features

### Image Display
- Supports two image modes:
  1. Standard badge image
  2. QR code version
- Binary image format
- 104px width (standard)

### Text Display
- Company name: 0.6 text size
- Details: 0.5 text size
- Automatic text truncation
- Multi-line support

### Communication
- SigFox integration
- UART communication
- Status LED indication
- Battery status detection

## Usage Instructions

1. **Basic Display**:
   - App shows main badge view on launch
   - Personal info clearly visible
   - Image displayed on left side

2. **QR Code Toggle**:
   - Press A to switch to QR view
   - Press again to return to badge view
   - QR code can contain contact info

3. **SigFox Functions**:
   - Press B to activate SigFox
   - LED indicates transmission
   - Automatic status update

4. **View Management**:
   - C button switches views
   - Clean transitions
   - State persistence

## Technical Details

### Image Requirements
- Binary format
- 104px width
- E-ink optimized
- Two versions needed:
  1. badge-image.bin
  2. badge-image_QR.bin

### Display Parameters
- WIDTH: 296 pixels
- HEIGHT: 128 pixels
- Company section: 30px
- Details sections: 20px each
- Dynamic name height

### Communication
- UART: 9600 baud
- TX: Pin 0
- RX: Pin 1
- SigFox protocol support

## Error Handling

- Image load verification
- Communication timeouts
- Battery level monitoring
- State recovery
- Display refresh management

## Customization

### Modifying Display
1. Update image files
2. Edit default text
3. Adjust text sizes
4. Configure layout constants

### Image Creation
1. Prepare 104px width image
2. Convert to binary format
3. Create QR version
4. Place in root directory

## Power Management

- Battery detection
- LED power control
- Display refresh optimization
- Sleep mode support
- Wake-up handling 