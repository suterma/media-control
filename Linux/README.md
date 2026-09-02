# Linux media control for Replayer (Experimental)

A simple python script that maps some of the existing [Replayer keyboard shortcuts](https://replayer.app/en/documentation/keyboard-shortcuts) to system media events.

NOTE: Currently, only Play/Pause is (experimentally) supported, as Replayer does not yet provide extensive media control itself.

## Usage

### Installation

    # After installing Python itself, install evdev to handle keyboard input events
    sudo apt install python3-evdev
    
    # Get the script
    wget https://github.com/suterma/media-control/raw/refs/heads/main/Linux/replayer-keymap.py 

    # Make it executable
    chmod +x replayer-keymap.py

### Startup

    # Privileged execution is necessary to get access to keyboard input
    sudo ./replayer-keymap.py

    Output should be like:

    Using keyboard: Logitech MX Keys
    Device: /dev/input/event4
    Starting Replayer key mapping ...
    Press Ctrl+C to stop.
    Mapping active.


### Shutdown

Simply press CRTL+C or close the terminal window.

## Technical details
    
    Physical keyboard
          │
          ▼
       evdev
          │
          │  Numpad /  ──────► KEY_PREVIOUSSONG
          │  Numpad *  ──────► KEY_NEXTSONG
          │  Numpad -  ──────► KEY_VOLUMEDOWN
          │  Numpad +  ──────► KEY_VOLUMEUP
          │  Numpad Enter ───► KEY_PLAYPAUSE
          │
          ▼
       uinput
          │
          ▼
    Linux input subsystem
          │
          ├── browser
          ├── media player
          ├── desktop environment
          └── any other interested application
    