# System Architecture

## System Startup Order

1. **Initial Boot**
   ```
   Power On/Wake
   └── main.py
       └── launcher.py (Main System Launcher)
   ```

2. **System Initialization**
   ```
   launcher.py
   ├── Hardware Initialization
   │   ├── Battery ADC setup
   │   ├── Display initialization
   │   └── Button setup
   │
   ├── State Management
   │   ├── Load previous state
   │   └── Check wake condition
   │
   └── Menu System Launch
   ```

## System Hierarchy

```
BadgerBadge System
│
├── Core System (badger_os.py)
│   ├── State Management
│   │   ├── state_save()
│   │   ├── state_load()
│   │   └── state_modify()
│   │
│   ├── Hardware Management
│   │   ├── get_battery_level()
│   │   └── get_disk_usage()
│   │
│   └── App Management
│       ├── launch()
│       ├── state_launch()
│       └── state_running()
│
├── Launcher (launcher.py)
│   ├── Menu System
│   │   ├── Page Navigation
│   │   └── App Selection
│   │
│   └── System Status
│       ├── Battery Display
│       └── Disk Usage
│
└── Applications
    ├── Core Apps
    │   ├── Badge (_badge.py)
    │   ├── List (_list.py)
    │   └── Image (_image.py)
    │
    ├── Utility Apps
    │   ├── Timer (_timer.py)
    │   ├── Temperature (_temp.py)
    │   └── Elevation (_elevation.py)
    │
    ├── Focus Apps
    │   └── Focus (_focus.py)
    │
    └── Emergency Apps
        ├── Medical (_medical.py)
        ├── Help (_help.py)
        └── Comms (_comms.py)
```

## State Management

```
State System
├── Global State (/state/launcher.json)
│   ├── Current Page
│   ├── Font Size
│   ├── Display Inversion
│   └── Running App
│
└── App States (/state/*.json)
    ├── Timer State
    ├── Focus State
    └── Other App States
```

## Hardware Control Layer

```
Hardware Layer
├── Display (badger2040.py)
│   ├── E-ink Display
│   └── LED Control
│
├── Power Management
│   ├── Battery Monitoring
│   └── Sleep/Wake System
│
├── Input System
│   ├── Button A
│   ├── Button B
│   └── Button C
│
└── Sensors
    ├── BME680 (Environment)
    └── SigFox (Communications)
```

## App Launch Flow
```
User Input → Launcher
             │
             ├── Check State
             │   ├── Load Previous App (if waking)
             │   └── or Start Fresh
             │
             ├── Launch App
             │   ├── Initialize App State
             │   ├── Setup Display
             │   └── Start Main Loop
             │
             └── Monitor Exit Condition (A+C buttons)
                 └── Return to Launcher
``` 