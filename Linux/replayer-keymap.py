#!/usr/bin/env python3

# A simple keyboard mapper for Replayer media controls on Linux.
# See https://github.com/suterma/media-control/tree/main/Linux
# 
# Specifically, the script:
# * automatically finds keyboards containing the mapped Numpad keys
# * doesn't rely on /dev/input/event4
# * grabs the physical keyboard
# * creates a virtual keyboard with the necessary key capabilities
# * forwards ordinary keyboard events
# * translates your five Numpad keys into native Linux media events
# * forwards EV_LED so Num Lock/Caps Lock state remains usable
# * cleans up properly on Ctrl+C/SIGTERM
#
# This script has mostly been provided by ChatGPT, with some manual modifications.


import signal
import sys

from evdev import InputDevice, UInput, ecodes, list_devices


# Maps Numpad Keys to media events
# Implements the shortcuts as per https://replayer.app/en/documentation/keyboard-shortcuts

# Numpad key -> Linux media key
MAPPING = {
    ecodes.KEY_KPSLASH:    ecodes.KEY_PREVIOUSSONG,
    ecodes.KEY_KPASTERISK: ecodes.KEY_NEXTSONG,
    ecodes.KEY_KPMINUS:    ecodes.KEY_VOLUMEDOWN,
    ecodes.KEY_KPPLUS:     ecodes.KEY_VOLUMEUP,
    ecodes.KEY_KPENTER:    ecodes.KEY_PLAYPAUSE,
}


def find_keyboard():
    """
    Find a keyboard containing all keys we want to remap.

    We deliberately don't depend on a fixed /dev/input/eventX number,
    since those can change between boots and on different machines.
    """
    required_keys = set(MAPPING)

    for path in list_devices():
        try:
            device = InputDevice(path)
            capabilities = device.capabilities()

            if ecodes.EV_KEY not in capabilities:
                device.close()
                continue

            keys = set(capabilities[ecodes.EV_KEY])

            if required_keys.issubset(keys):
                return device

            device.close()

        except OSError:
            pass

    return None



def build_uinput_capabilities(device):
    """
    Build capabilities for the virtual keyboard.

    We only copy the event types that make sense for a keyboard,
    rather than blindly passing all of the physical device's
    capabilities to UInput.
    """

    physical = device.capabilities()

    capabilities = {}

    # Forward keyboard events.
    if ecodes.EV_KEY in physical:
        keys = set(physical[ecodes.EV_KEY])

        # Add the media keys we generate.
        keys.update(MAPPING.values())

        capabilities[ecodes.EV_KEY] = list(keys)

    # Preserve LEDs such as Num Lock and Caps Lock.
    if ecodes.EV_LED in physical:
        capabilities[ecodes.EV_LED] = physical[ecodes.EV_LED]

    # Preserve autorepeat settings if the physical keyboard has them.
    if ecodes.EV_REP in physical:
        capabilities[ecodes.EV_REP] = physical[ecodes.EV_REP]

    return capabilities


def main():
    device = find_keyboard()

    if device is None:
        print("Could not find a keyboard with the required Numpad keys.")
        sys.exit(1)

    print(f"Using keyboard: {device.name}")
    print(f"Device: {device.path}")
    print("Starting Replayer key mapping ...")
    print("Press Ctrl+C to stop.")

    capabilities = build_uinput_capabilities(device)

    try:
        ui = UInput(
            capabilities,
            name="Replayer Media Numpad",
            vendor=0x0001,
            product=0x0001,
            version=1,
        )
    except Exception:
        device.close()
        raise

    grabbed = False

    def cleanup(signum=None, frame=None):
        nonlocal grabbed

        print("\nStopping Replayer key mapping ...")

        if grabbed:
            try:
                device.ungrab()
            except OSError:
                pass

        try:
            ui.close()
        except OSError:
            pass

        try:
            device.close()
        except OSError:
            pass

        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    try:
        # Stop the original physical keyboard events from reaching
        # applications. We will reproduce them through uinput.
        device.grab()
        grabbed = True

        print("Mapping active.")

        for event in device.read_loop():

            if event.type == ecodes.EV_KEY:
                output_code = MAPPING.get(event.code, event.code)

                ui.write(
                    ecodes.EV_KEY,
                    output_code,
                    event.value,
                )
                ui.syn()

            elif event.type == ecodes.EV_LED:
                # Forward Num Lock / Caps Lock / Scroll Lock changes.
                ui.write(
                    event.type,
                    event.code,
                    event.value,
                )
                ui.syn()

            elif event.type == ecodes.EV_SYN:
                # read_loop() normally handles synchronization for us,
                # so we don't need to forward EV_SYN explicitly.
                pass

            else:
                # Forward other supported events.
                try:
                    ui.write(
                        event.type,
                        event.code,
                        event.value,
                    )
                    ui.syn()
                except OSError:
                    # Ignore event types that the virtual device
                    # doesn't support.
                    pass

    except KeyboardInterrupt:
        cleanup()

    except OSError as e:
        print(f"\nInput device error: {e}", file=sys.stderr)
        cleanup()


if __name__ == "__main__":
    main()