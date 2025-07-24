import numpy as np
import rtmidi
from rtmidi.midiconstants import (CONTROL_CHANGE)

previousNote = None

midiout = rtmidi.MidiOut()
port_index = None
available_ports = midiout.get_ports()

for i, port in enumerate(available_ports):
    if "python port" in port.lower():
        port_index = i
        break

midiout.open_port(port_index)

def take_finger_data(left, right, client):

    handle_left(left, client)
    handle_right(right, client)

def handle_left(leftFingerData, client):

    if leftFingerData is None:
        client.send_message("/live/track/set/mute", [1, 1])  # track 2 (kick), mute on
        client.send_message("/live/track/set/mute", [2, 1])  # track 3 (snare), mute on
        client.send_message("/live/track/set/mute", [3, 1])  # track 4 (clap), mute on
        client.send_message("/live/track/set/mute", [4, 1])  # track 5 (hi-hat), mute on
        client.send_message("/live/track/set/mute", [5, 1])  # track 6 (bell), mute on

        return
    
    magnitude = leftFingerData.magnitude

    if magnitude == 1:
        client.send_message("/live/track/set/mute", [4, 0])  # track 2 (kick), mute off
        client.send_message("/live/track/set/mute", [2, 1])  # track 3 (snare), mute on
        client.send_message("/live/track/set/mute", [3, 1])  # track 4 (clap), mute on
        client.send_message("/live/track/set/mute", [4, 1])  # track 5 (hi-hat), mute on
        client.send_message("/live/track/set/mute", [5, 1])  # track 6 (bell), mute on
        
    elif magnitude == 2:
        client.send_message("/live/track/set/mute", [1, 0])  # track 2 (kick), mute off
        client.send_message("/live/track/set/mute", [2, 0])  # track 3 (snare), mute off
        client.send_message("/live/track/set/mute", [3, 1])  # track 4 (clap), mute on
        client.send_message("/live/track/set/mute", [4, 1])  # track 5 (hi-hat), mute on
        client.send_message("/live/track/set/mute", [5, 1])  # track 6 (bell), mute on

    elif magnitude == 3:
        client.send_message("/live/track/set/mute", [1, 0])  # track 2 (kick), mute off
        client.send_message("/live/track/set/mute", [2, 0])  # track 3 (snare), mute off
        client.send_message("/live/track/set/mute", [3, 0])  # track 4 (clap), mute off
        client.send_message("/live/track/set/mute", [4, 1])  # track 5 (hi-hat), mute on
        client.send_message("/live/track/set/mute", [5, 1])  # track 6 (bell), mute on

    elif magnitude == 4:
        client.send_message("/live/track/set/mute", [1, 0])  # track 2 (kick), mute off
        client.send_message("/live/track/set/mute", [2, 0])  # track 3 (snare), mute off
        client.send_message("/live/track/set/mute", [3, 0])  # track 4 (clap), mute off
        client.send_message("/live/track/set/mute", [4, 0])  # track 5 (hi-hat), mute off
        client.send_message("/live/track/set/mute", [5, 1])  # track 6 (bell), mute on

    elif magnitude == 5:
        client.send_message("/live/track/set/mute", [1, 0])  # track 2 (kick), mute off
        client.send_message("/live/track/set/mute", [2, 0])  # track 3 (snare), mute off
        client.send_message("/live/track/set/mute", [3, 0])  # track 4 (clap), mute off
        client.send_message("/live/track/set/mute", [4, 0])  # track 5 (hi-hat), mute off
        client.send_message("/live/track/set/mute", [5, 0])  # track 6 (bell), mute off
    


def handle_right(rightFingerData, client):

    global previousNote

    if rightFingerData is None:

        if previousNote is not None:
            midiout.send_message([0x80, previousNote, 0])
            previousNote = None

        return
    
    # 1 lowest segment, 4 highest

    segmentEffects = {
        1: "plain",
        2: "chord", 
        3: "vocoder", 
        4: "eq" 
    }

    magnitutudeMidiNotes = {
        1: 36,  # C2
        2: 40,  # E2
        3: 41,  # F2
        4: 45,  # A2
        5: 48   # C3
    }

    segment = rightFingerData.segment
    magnitude = rightFingerData.magnitude

    if previousNote and previousNote != magnitutudeMidiNotes[magnitude]:
        midiout.send_message([0x80, previousNote, 0])
    
    if previousNote != magnitutudeMidiNotes[magnitude]:
        note_on = [0x90, magnitutudeMidiNotes[magnitude], 100]
        midiout.send_message(note_on)
        previousNote = magnitutudeMidiNotes[magnitude]

    deviceToActivate = segmentEffects[segment]

    if deviceToActivate == "plain":

        # track 6 turn device 0, 2, 3 off
        client.send_message("/live/device/set/parameter/value", [6, 0, 0, 0])
        client.send_message("/live/device/set/parameter/value", [6, 2, 0, 0])
        client.send_message("/live/device/set/parameter/value", [6, 3, 0, 0])

    elif deviceToActivate == "chord":

        # track 6 turn device 0 on
        client.send_message("/live/device/set/parameter/value", [6, 0, 0, 1])

        # track 6 turn device 2, 3 off
        client.send_message("/live/device/set/parameter/value", [6, 2, 0, 0])
        client.send_message("/live/device/set/parameter/value", [6, 3, 0, 0])

    elif deviceToActivate == "vocoder":
        # track 6 turn device 0, 2 on
        client.send_message("/live/device/set/parameter/value", [6, 0, 0, 1])
        client.send_message("/live/device/set/parameter/value", [6, 2, 0, 1])

        # track 6 turn device 3 off
        client.send_message("/live/device/set/parameter/value", [6, 3, 0, 0])


    elif deviceToActivate == "eq":
        # track 6 turn device 0,2,3 on
        client.send_message("/live/device/set/parameter/value", [6, 0, 0, 1])
        client.send_message("/live/device/set/parameter/value", [6, 2, 0, 1])
        client.send_message("/live/device/set/parameter/value", [6, 3, 0, 1])

