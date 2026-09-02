# media-control
Various media controller implementations as support for [Replayer](https://replayer.app).

## Linux (Experimental)

A simple python script maps some of the existing [keyboard shortcuts](https://replayer.app/en/documentation/keyboard-shortcuts) to media events on a virtual keyboard.

Currently, only Play/Pause is (experimentally) supported, as Replayer does not yet provide extensive media control itself.

### Usage

#### Installation

    # Install Python itself, if necessary, then install
    sudo apt install python3-evdev
    
    # Get the script

    # Make it executable
    chmod +x replayer-keymap.py

#### Startup

    sudo ./replayer-keymap.py

#### Shutdown


### Technical details
    
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
    