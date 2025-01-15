# Focus App Documentation

The Focus app is a Pomodoro-style timer that uses a traffic light system to help manage focus and break periods. It's designed to help with concentration and time management.

## Features

- Traffic light visualization system
- Multiple preset focus durations
- Visual countdown display
- Configurable focus and break periods
- State persistence between sessions
- Audio/visual alerts at period changes

## Interface

### Display Elements
- Traffic light indicator (Red, Orange, Green)
- Time remaining display
- Current mode indicator
- Progress bar
- Battery status

### Controls
- **Button A**: Previous option/Decrease time
- **Button B**: Select/Start/Pause
- **Button C**: Next option/Increase time
- **A + C**: Exit to main menu

## Configuration

The app is configured through `focus.txt` with different presets for each badge variant.

### Badge Eva Configuration
\`\`\`
Focus 60 mins
3600    # Red phase (60 mins)
1800    # Orange phase (30 mins)
Focus 30 mins
1800    # Red phase (30 mins)
900     # Orange phase (15 mins)
Huiswerk 12/2
720     # Red phase (12 mins)
120     # Orange phase (2 mins)
Manual
\`\`\`

### Badge Papa Configuration
\`\`\`
Focus 50 mins
3000    # Red phase (50 mins)
600     # Orange phase (10 mins)
Focus 25 mins
1500    # Red phase (25 mins)
300     # Orange phase (5 mins)
Focus 12 mins
720     # Red phase (12 mins)
120     # Orange phase (2 mins)
\`\`\`

## Operation Modes

### Traffic Light System
1. **Red Light**: Main focus period
   - No interruptions allowed
   - Full concentration required

2. **Orange Light**: Transition period
   - Light interruptions acceptable
   - Reduced focus acceptable

3. **Green Light**: Break period
   - Focus session complete
   - Free to take a break

### Preset Modes

#### Badge Eva
1. **60/30**: 60 minutes focus, 30 minutes transition
2. **30/15**: 30 minutes focus, 15 minutes transition
3. **12/2**: 12 minutes focus, 2 minutes transition
4. **Manual**: Custom duration setting

#### Badge Papa
1. **50/10**: 50 minutes focus, 10 minutes transition
2. **25/5**: 25 minutes focus, 5 minutes transition
3. **12/2**: 12 minutes focus, 2 minutes transition

## Usage Instructions

1. **Starting a Session**:
   - Select desired preset using A/C buttons
   - Press B to start the timer
   - Red light indicates focus period has begun

2. **During a Session**:
   - Display shows remaining time
   - Traffic light indicates current phase
   - Progress bar shows overall progress

3. **Transitions**:
   - Automatic transition between phases
   - Visual alert when phase changes
   - Optional sound alerts (if enabled)

4. **Ending a Session**:
   - Green light indicates completion
   - Option to restart or select new duration
   - Exit using A+C combination

## Technical Details

- Uses system timer for accurate timing
- State saved in JSON format
- Efficient e-ink display updates
- Low power consumption design

## Error Handling

- Graceful handling of power loss
- State recovery on wake from sleep
- Invalid input protection
- Battery level monitoring 