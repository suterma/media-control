# Windows media control for Replayer (Experimental)

A custom [AutoHotkey](https://www.autohotkey.com/) mapping, that maps some of the existing [keyboard shortcuts](https://replayer.app/en/documentation/keyboard-shortcuts) to Windows virtual key codes for media control.

Currently, only Play/Pause is (experimentally) supported, as Replayer does not yet provide extensive media control itself.


## Usage

### Installation

[Download AutoHotkey](https://www.autohotkey.com/download/). You might run the installer EXE, or just extract the portable version from their ZIP distribution.

    # Get the script, in PowerShell:
    Invoke-WebRequest -Uri 'https://github.com/suterma/media-control/raw/refs/heads/main/Windows/replayer.ahk'  

### Startup

    # Privileged execution is necessary to get access to keyboard input
    ./AutoHotkey64.exe replayer.ahk

### Shutdown

Close the AutoHotkey UI window.

