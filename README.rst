======================================================
PY3-MIDI PACKAGE
======================================================

*Created by Edouard Theron* 

ed [at] edtheron [dot] me

*February 2017*

**Published under GNU License**

.. sectum::
.. contents:: Table of Contents


Package for using MIDI standard with Python3


1) PURPOSE
***********
This Python3 library has been made in order to communicate easily with any MIDI devices. The only requirement is to have a serial
interface on your computer. It's on this interface that you must connect MIDI cables to establish a communication between your
machine and the MIDI devices.

The py3-midi package allows users to build and/or read MIDI messages without having to worry on formating them before sending and/or after receiving.

MIDI (Musical Instrument Digital Interface) is a standard making easy for instruments, computers and other electronic devices
to communicate.

This library is able to deal with any kind of MIDI messages, on any of the 16 possible channels.

For more details on the MIDI standard, see Wikipedia MIDI page https://en.wikipedia.org/wiki/MIDI

2) INSTALLATION
***************
You can install easily the package using Python Package Index. You just have to run the following command::

	$ python3 -m pip install py3-midi

Then you can import it with the directive::

	import midi

3) CONTENT OF THE LIBRARY
*************************
A) Class MidiConnector
======================
Creates an interface between your program and the serial port of the machine. You instanciate by giving the path to the serial port.
Example .. highlightlang::

	c = MidiConnector('/dev/serial0') # should be the path on RaspberryPi 3

If you *don't want* the MidiConnector.read() method to block for ever if it receives nothing, use the keyword argument **timeout** to set up a 
maximum duration (seconds) of blocking .. highlightlang::

	c = MidiConnector('/dev/serial0', timeout=5) 

*(Note: The timeout is only used for reading, not writing)*

B) Class Message
================

C) Classes for different type of MIDI messages
==============================================
4) EXAMPLES
*************
Before doing anything, import the package to your script::

	import midi

Then depending on what you need to do, follow these examples.

A) Reading MIDI messages (via MIDI IN device)

First, I need to set up a connector object. It requires at least one argument: the port used for the serie interface::

	cnx = midi.Connector('path/to/serial/port')

Super easy. Now I just have to read through it::

	msgIn = cnx.read() # returns any MIDI messages received

Note that this will block until a MIDI message is received (thus it can block for ever if your loop is not properly set up)
To set a timeout, you need to specify it when building the connector::

	cnxWithTimeout = midi.Connector('path/to/serial/port', timeout=10) 
	# will block for max 10 sec when reading, or until a message is received 

You can also specify a channel for listening::

	msgInChannel8 = cnx.read(8) # returns MIDI messages received on channel 8 only, and ignores the rest

B) Sending MIDI messages (via MIDI OUT device)

First you need to create the type of message you need to send (either a Control Change, a Note On, etc...)

Let's say I want to create a Control Change that sets the value 127 to the control number 12::

	cc = midi.ControlChange(12, 127)

I want to send the message on channel 15::

	channel = 15

Now I have everything I need to build up a MIDI message::

	msgOut = Message(cc, channel)

I create the connector for sending it (of course!)::

	cnx = midi.Connector('path/to/serial/port'):
	cnx.write(msgOut)