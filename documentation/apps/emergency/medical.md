# Medical App Documentation

The Medical app provides quick access to essential medical information and emergency details. It's designed to be easily readable and accessible in emergency situations.

## Features

- Essential medical information display
- Quick access interface
- Clear, high-contrast display
- Emergency contact information
- Age calculation
- Configurable details

## Interface

### Display Elements
- Personal information
- Medical details
- Emergency contacts
- Battery status
- Navigation indicators

### Controls
- **Button A**: Previous page/section
- **Button B**: Select/Confirm
- **Button C**: Next page/section
- **A + C**: Exit to main menu

## Configuration

The app is configured through `medical.txt` with different information for each badge variant.

### Badge Eva Configuration
\`\`\`
Name: John Doe
Date of Birth: 01-06-2016
Blood Type: -
Allergies: None
Medications: None
Length: 140 cm
Weight: 30 kg
Donor: No
Current year: 2024
\`\`\`

### Badge Papa Configuration
\`\`\`
Name: John Doe
Date of Birth: 01-06-1974
Blood Type: B+
Allergies: None
Medications: None
Length: 185 cm
Weight: 81 kg
Donor: No
Current year: 2024
\`\`\`

## Information Categories

### Personal Information
- Full name
- Date of birth
- Current age (auto-calculated)
- Height and weight

### Medical Details
- Blood type
- Allergies
- Current medications
- Organ donor status

## Usage Instructions

1. **Accessing Information**:
   - Launch Medical app from menu
   - Information displayed immediately
   - Use A/C to navigate multiple pages

2. **Updating Information**:
   - Edit `medical.txt` file
   - Follow exact format
   - Restart app to apply changes

3. **Emergency Use**:
   - Quick access from any screen
   - Clear, large text display
   - Essential info on first page

## Technical Details

- Text-based configuration
- Automatic age calculation
- State persistence
- Low power display mode
- Emergency priority access

## Security Considerations

- Public/Private information separation
- Optional information masking
- Emergency access protocol
- Data protection measures

## Customization

### Editing Medical Information
1. Open `medical.txt`
2. Update relevant fields
3. Maintain exact format
4. Save changes
5. Restart app

### Required Fields
- Name (string)
- Date of Birth (DD-MM-YYYY)
- Blood Type (string)
- Allergies (string)
- Medications (string)
- Length (number + cm)
- Weight (number + kg)
- Donor (Yes/No)
- Current year (YYYY)

## Error Handling

- Invalid data protection
- Format validation
- Missing field handling
- Update verification
- Error notifications

## Privacy Notes

- Consider privacy when displaying information
- Optional field masking available
- Emergency access protocols
- Data security measures 