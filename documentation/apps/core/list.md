# List App Documentation

The List app provides a customizable checklist functionality, perfect for daily tasks, school items, or any other list-based needs. It features an interactive checkbox system and persistent state management.

## Features

- Interactive checklist
- Customizable items
- Checkbox interaction
- State persistence
- Scrollable interface
- Visual navigation aids

## Interface

### Display Elements
- Title ("Heb ik alles?")
- Scrollable item list
- Navigation arrows
- Checkboxes
- Selection indicator
- Battery status

### Display Layout
- List starts at 40 pixels from top
- Arrow thickness: 3 pixels
- Arrow width: 18 pixels
- Arrow height: 14 pixels
- List padding: 2 pixels

### Controls
- **Button A**: Move up/Previous
- **Button B**: Toggle checkbox
- **Button C**: Move down/Next
- **A + C**: Exit to main menu

## Configuration

The app is configured through `checklist.txt` with a simple line-by-line format.

### Default List Format
\`\`\`
Item 1
Item 2
Item 3
..etc
\`\`\`

### Display Parameters
- Maximum item characters: 26
- Title text size: 0.7
- Item text size: 0.6
- Item spacing: 20 pixels
- List width: Screen width - padding - arrow width

## Features

### List Management
- Add/remove items via text file
- Check/uncheck items
- Scroll through long lists
- State persistence between sessions

### Visual Elements
- Up/down arrows for navigation
- Checkbox indicators
- Highlighted current selection
- Clear item separation

### State Management
- Saves checked state
- Preserves scroll position
- Maintains selection
- Recovers after power loss

## Usage Instructions

1. **Navigation**:
   - Use A/C buttons to move up/down
   - Current selection is highlighted
   - Arrows indicate scroll direction
   - Automatic scroll for long lists

2. **Checking Items**:
   - Press B to toggle checkbox
   - Visual feedback on toggle
   - State saved automatically
   - Clear check/uncheck indication

3. **List Management**:
   - Edit checklist.txt for changes
   - One item per line
   - No special formatting needed
   - Restart app to load changes

## Technical Details

### Text Requirements
- Plain text format
- One item per line
- Maximum 26 characters per item
- UTF-8 encoding

### Display Parameters
- List area: WIDTH - 4 - ARROW_WIDTH
- Visible items: Based on screen height
- Automatic scrolling
- Smooth navigation

### State Storage
- JSON format
- Persistent storage
- Automatic recovery
- Efficient updates

## Error Handling

- File read verification
- Invalid format protection
- State recovery
- Boundary checking
- Display refresh management

## Customization

### Modifying List
1. Open `checklist.txt`
2. Add/remove/edit items
3. Save file
4. Restart app

### Format Requirements
- Text file format
- Line-separated items
- No special characters needed
- Length limits enforced

## Performance

- Optimized scrolling
- Efficient state updates
- Memory-conscious design
- Quick response time
- Power-efficient operation 