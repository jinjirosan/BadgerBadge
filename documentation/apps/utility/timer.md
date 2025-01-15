# Timer App Documentation

The Timer app provides customizable countdown timers for various daily activities. It features visual progress bars and configurable presets for different tasks.

## Features

- Multiple preset activities
- Visual countdown display
- Progress bar indication
- Configurable durations
- State persistence
- Visual/audio completion alerts

## Interface

### Display Elements
- Activity name
- Time remaining
- Progress bar
- Battery status
- Current state indicator

### Controls
- **Button A**: Previous activity
- **Button B**: Start/Pause timer
- **Button C**: Next activity
- **A + C**: Exit to main menu

## Configuration

The app is configured through `timer.txt` with different presets for each badge variant.

### Badge Eva Configuration (Daily Routines)
\`\`\`
aankleden       # Getting dressed
900             # 15 minutes
ontbijt         # Breakfast
960             # 16 minutes
schoenen        # Shoes
300             # 5 minutes
douchen         # Shower
1200            # 20 minutes
pootjes wassen  # Washing feet
720             # 12 minutes
pyama           # Pajamas
420             # 7 minutes
\`\`\`

### Badge Papa Configuration (General Timers)
\`\`\`
Japanse Thee    # Japanese Tea
150             # 2.5 minutes
Presentatie 18  # Presentation 18
1080            # 18 minutes
Timer 5         # 5-minute timer
300             # 5 minutes
Timer 10        # 10-minute timer
600             # 10 minutes
Timer 15        # 15-minute timer
900             # 15 minutes
Timer 20        # 20-minute timer
1200            # 20 minutes
\`\`\`

## Operation Modes

### Badge Eva Mode
- Focused on daily routine activities
- Sequential task timing
- Child-friendly activity names
- Routine-based organization

### Badge Papa Mode
- General-purpose timing
- Presentation timing
- Tea brewing timer
- Flexible duration presets

## Usage Instructions

1. **Selecting an Activity**:
   - Use A/C buttons to cycle through activities
   - Current activity name displayed
   - Duration shown below name

2. **Starting Timer**:
   - Press B to start countdown
   - Progress bar begins filling
   - Time remaining displayed

3. **During Countdown**:
   - Progress bar updates continuously
   - Time updates every second
   - Can pause/resume with B button

4. **Timer Completion**:
   - Visual indication when complete
   - Optional audio alert
   - Returns to activity selection

## Technical Details

- Time tracking using system timer
- State persistence in JSON format
- Optimized display updates
- Low power operation
- Activity configurations in text file

## Error Handling

- Power loss recovery
- Invalid duration protection
- State preservation
- Battery monitoring
- Error messaging

## Customization

### Adding/Modifying Activities
1. Open `timer.txt`
2. Add activity name (first line)
3. Add duration in seconds (second line)
4. Save file
5. Restart app to load changes

### Duration Format
- All times specified in seconds
- Minimum duration: 30 seconds
- Maximum duration: 3600 seconds (1 hour)
- Invalid durations default to 300 seconds 