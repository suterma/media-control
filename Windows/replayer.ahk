#Requires AutoHotkey v2.0

; Maps Numpad Keys to Windows multimedia virtual-key codes
; Implements the shortcuts as per https://replayer.app/en/documentation/keyboard-shortcuts

NumpadDiv::Send "{vkB1}"       ; Previous Track  / VK_MEDIA_PREV_TRACK
NumpadMult::Send "{vkB0}"      ; Next Track      / VK_MEDIA_NEXT_TRACK
NumpadSub::Send "{vkAE}"       ; Volume Down     / VK_VOLUME_DOWN
NumpadAdd::Send "{vkAF}"       ; Volume Up       / VK_VOLUME_UP
NumpadEnter::Send "{vkB3}"     ; Play/Pause      / VK_MEDIA_PLAY_PAUSE