# fingerstring

a concept seen much before just my own implementation from scratch - hand controlled music.

This project uses opencv camera capture, tensorflow/mediapipe hand recognition and the rtmidi python library to capture the "magnitude" of the right/left hand's index and thumb pinch gesture. 

Along with this it also adds variation to the music dependant on the area of the capture the hand is in (dependent on y level).

I ran this on my Windows machine, using Ableton live as a DAW in the background for the music and midi control.

Along with this, I used the application loopMIDI with a midi port named "python port" and a digital control interface for ableton called "AbletonOSC".

The right hand controls a synth and the pinch its note played, and the y position on screen turns off and on various audio effects.

The left hand controls drums and adds more layers of drum dependent on the pinch.


## running on your own machine

This was designed for Ableton Live (tested on Ableton Live 11 Suite), but perhaps works with other DAWs, not tested though. If you wish to run on your own machine, launch loopMIDI, create a port named "python port". Have AbletonOSC downloaded and when you launch ableton, go to the Options>Preferences>Link/Tempo/MIDI then add a control surface and select AbletonOSC

Also for MIDI ports then add python port as in for track and remote.

Use the same ableton live project I created (found within this repository) abletonSet Project > abletonSet.als 

And should work!!!!

## Example video

Video can be found in files as exampleVideo.mp4