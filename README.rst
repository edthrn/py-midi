=================
PY-MIDI LIBRARY
=================

**A library for communicating via MIDI standard using Python3**

*Warning: To use with Python3 only*. The library doesn't work with Python2.

*Published under GNU License*

**This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY**

Do not hesitate to use Issues if necessary.

ed [at] edtheron [dot] me

.. sectum::
.. contents:: Table of Contents

1) PURPOSE
***********
This Python3 library has been made in order to communicate easily with any MIDI devices. The only requirement is to have a serial
interface on your computer. It's on this interface that you must connect MIDI cables to establish a communication between your
machine and the MIDI devices.

The py-midi library allows users to build and/or read MIDI messages without having to worry on formating them before sending and/or after receiving.

MIDI (Musical Instrument Digital Interface) is a standard used for making easy for instruments, computers and other electronic devices
to communicate.

This library is able to deal with any kind of MIDI messages, on any of the 16 possible channels.

For more details on the MIDI standard, see Wikipedia MIDI page https://en.wikipedia.org/wiki/MIDI

2) INSTALLATION
***************
You can install easily the package using Python Package Index. You just have to run the following command::

	$ python3 -m pip install py-midi

or::

	$ sudo pip3 install py-midi

Then you can import the package to your program::

	import midi

3) CONTENT OF THE LIBRARY
*************************
A) Class MidiConnector
======================
Creates an interface between your program and the serial port of the machine. You instanciate by giving the path to the serial port. Example::

	c = MidiConnector('/dev/serial0') # should be the path used on RaspberryPi 3

If you *don't want* the MidiConnector.read() method to block for ever if it receives nothing, use the keyword argument **timeout** to set up a maximum duration (seconds) of blocking::

    c = MidiConnector('/dev/serial0', timeout=5)

*(Note: The timeout is only used for reading, not for writing)*

For reading messages received via MIDI IN, use the method read() as follow::

    msg = c.read()

For sending messages via MIDI OUT::

    c.write(msg)

By default, reading is done in **OMNI** mode, whereas writing is specific to a channel. However, you can override the default
behavior. For further details, run::

    help(MidiConnector)


B) Classes for different type of MIDI messages
==============================================
8 types of MIDI message (including SysEx) are managed by the package.
Here are the exhaustive list, as well as how to instanciate them.
*Note: none of the arguments passed to instanciate a message type must exceed 127 (255 if SysEx data), or be negative*

* NoteOff(note_number, velocity)
* NoteOn(note_number, velocity)
* PolyphonicAftertouch(note_number, pressure)
* ChannelAftertouch(pressure)
* ControlChange(control_number, value)
* ProgramChange(program_number)
* PitchWheel(least_signifcant_byte, most_significant_byte)
* SysEx(manufacturer_id, data1, data2..., data-N)

C) Class Message
================
Represents a MIDI message, with all its properties:

+--------------+------------------------------------------------------------+
| Attribute    |  Represents                                                |
+==============+============================================================+
| type         | The type of MIDI message: ControlChange, ProgramChange,    |
|              | NoteOff, NoteOn, etc...                                    |
+--------------+------------------------------------------------------------+
| channel      | The channel used to send or the channel on which it has    |
|              | been sent (from 1 to 16)                                   |
+--------------+------------------------------------------------------------+
| status       | The value of first message byte                            |
|              |                                                            |
+--------------+------------------------------------------------------------+
| data1        | The value of second message byte                           |
|              |                                                            |
+--------------+------------------------------------------------------------+
| data2        | The value of third message byte                            |
|              | *Note: some types carry only 2 bytes*                      |
+--------------+------------------------------------------------------------+

If you want to build a MIDI message, you need to use positionnal arguments, first the type, then the channel::

    note_on = NoteOn(68, 102)
    channel = 1
    msg = Message(note_on, channel)

Then you can access other properties, e.g. for a message type NoteOn::
    >>> msg.velocity
    102
    >>> hex(msg.status) # The first byte of a NoteOn sent on channel 1 will be 1001 0000
    '0x90'


4) EXAMPLES
*************
Before doing anything, import the package to your program::

	import midi

Then depending on what you need to do, follow these examples.

A) Reading MIDI messages (via MIDI IN device)
=============================================

First, I need to set up a connector object. It requires at least one argument: the port used for the serie interface::

	c = midi.Connector('path/to/serial/port')

Super easy. Now I just have to read through it::

	msgIn = c.read() # return any MIDI messages received

Note that this will block until a MIDI message is received (thus it can block for ever if your loop is not properly set up)
To set a timeout, you need to specify it when building the connector::

	c_timeout = midi.Connector('path/to/serial/port', timeout=10)
	# will block for max 10 sec when reading, or until a message is received 

You can also specify a channel for listening::

	msgInChannel8 = c.read(8) # return MIDI messages received on channel 8 only. Ignore the rest

B) Sending MIDI messages (via MIDI OUT device)
==============================================

First you need to create the type of message you need to send (either a Control Change, a Note On, etc...)

Let's say I want to create a Control Change that sets the value 127 to the control number 12::

	cc = midi.ControlChange(12, 127)

I want to send the message on channel 15::

	channel = 15

Now I have everything I need to build up a MIDI message::

	msgOut = midi.Message(cc, channel)

I create the connector for sending the message (of course!)::

	c = midi.Connector('path/to/serial/port')
	c.write(msgOut)

Do not hesitate to read helpers for further details, for example::

	>>> help(midi.MidiConnector)