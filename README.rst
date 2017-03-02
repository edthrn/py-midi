Written by Edouard Theron 
February 2017

Package for using MIDI standard with Python3

TO BE COMPLETED...

1. PURPOSE
2. CONTENT
3. USECASES
	3.1 Reading MIDI messages (via MIDI IN)

First, you need to set up a connector object. It requires one argument only: the port used for the serie interface

cnx = midi.Connector('path/to/serial/port')

message = cnx.read() # returns any MIDI messages, sent on any channel
msg_on_channel_8 = cnx.read(8) # returns the MIDI messages sent on channel 8, ignores the rest

	3.2 Sending MIDI messages (via MIDI OUT)

First you need to create the type of message you need to send (either a Control Change, a Note On, etc...)

Let's say I want to create a Control Change thats sets the value 127 to the control number 12.

cc = midi.ControlChange(12, 127)

I want to send the message on channel 15

chan = 15

I create the connector

cnx = midi.Connector('path/to/serial/port')

cnx.write(chan, cc)