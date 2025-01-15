# Image App Documentation

The Image app provides a gallery viewer for displaying binary images on the e-ink display. It supports multiple images with navigation and includes a default BadgerPunk image.

## Features

- Image gallery functionality
- Multiple image support
- Navigation between images
- Binary image format
- Automatic image loading
- Default image included

## Interface

### Display Elements
- Full-screen image display
- Navigation overlay
- Image counter
- Battery status
- LED indication

### Display Layout
- Full screen: 296x128 pixels
- Overlay border: 40 pixels
- Overlay spacing: 20 pixels
- Overlay text size: 0.5

### Controls
- **Button A**: Previous image
- **Button B**: Toggle overlay
- **Button C**: Next image
- **A + C**: Exit to main menu

## Configuration

### Image Requirements
\`\`\`
- Resolution: 296x128 pixels
- Color depth: 1-bit (black and white)
- Format: Binary (.bin)
- Location: /images/ directory
\`\`\`

### Directory Structure
\`\`\`
/images/
  ├── image1.bin
  ├── image2.bin
  ├── image3.bin
  └── readme.txt
\`\`\`

## Features

### Image Management
- Automatic image discovery
- Sequential navigation
- Circular browsing
- Default image fallback
- Dynamic loading

### Visual Elements
- Full-screen display
- Navigation overlay
- Image counter
- Status indicators
- LED feedback

### File Handling
- Binary format support
- Automatic directory creation
- Default image installation
- Error handling
- Memory management

## Usage Instructions

1. **Viewing Images**:
   - Images display full-screen
   - Use A/C to navigate
   - B toggles information overlay
   - LED indicates activity

2. **Adding Images**:
   1. Convert images using converter tool
   2. Place .bin files in /images/
   3. Restart app to load new images
   4. Navigate using A/C buttons

3. **Image Conversion**:
   ```bash
   python3 convert.py --binary --resize image_file_1.png image_file_2.png
   ```

## Technical Details

### Image Format
- Binary format (.bin)
- 296x128 pixels exact
- 1-bit color depth
- Memory efficient
- Quick loading

### Display Parameters
- Full screen utilization
- Overlay for information
- LED status indication
- Efficient refresh

### File System
- Dedicated images directory
- Automatic setup
- File enumeration
- Error recovery

## Error Handling

- Missing directory creation
- Invalid file handling
- Memory management
- Load failure recovery
- Display refresh errors

## Customization

### Adding Images
1. Prepare image (296x128 px)
2. Convert to binary format
3. Copy to /images/
4. Restart application

### Image Requirements
- Exact dimensions required
- Binary format only
- Proper naming (.bin)
- Size optimization
- Memory constraints

## Performance

### Memory Management
- Efficient file loading
- Single image in memory
- Resource cleanup
- Garbage collection

### Display Optimization
- Quick image switching
- Minimal refreshes
- LED status feedback
- Power-efficient operation

## Image Conversion Tool

### Usage
```bash
python3 convert.py --binary --resize input_image.png
```

### Options
- --binary: Create binary output
- --resize: Auto-resize to screen
- Multiple file support
- Format conversion
- Size optimization 