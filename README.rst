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
~~~~~~~~~~
This Python3 library has been made in order to communicate easily with any MIDI devices. The only requirement is to have a serial
interface on your computer. It's on this interface that you must connect MIDI cables to establish a communication between your
machine and the MIDI devices.

The py3-midi package allows users to build and/or read MIDI messages without having to worry on formating them before sending and/or after receiving.

MIDI (Musical Instrument Digital Interface) is a standard making easy for instruments, computers and other electronic devices
to communicate.

This library is able to deal with any kind of MIDI messages (except SysEx for the moment, coming soon), on any of the 16 possible channels.

For more details on the MIDI standard, see Wikipedia MIDI page https://en.wikipedia.org/wiki/MIDI

2) CONTENT
~~~~~~~~~~
Some Content here.

3) USECASES
~~~~~~~~~~
A) Reading MIDI messages (via MIDI IN device)

First, I need to set up a connector object. It requires at least one argument: the port used for the serie interface::

	cnx = midi.Connector('path/to/serial/port')

Super easy. Now I just have to read through it::

	msgIn = cnx.read() # returns any MIDI messages received

or::

	msgInChannel8 = cnx.read(8) # returns MIDI messages received on channel 8 only, and ignores the rest

	B) Sending MIDI messages (via MIDI OUT device)

	First you need to create the type of message you need to send (either a Control Change, a Note On, etc...)

	Let's say I want to create a Control Change thats sets the value 127 to the control number 12::

		cc = midi.ControlChange(12, 127)

	I want to send the message on channel 15::

		channel = 15

	Now I have everything I need to build up a MIDI message::

		msgOut = Message(cc, channel)

	I create the connector for sending it (of course!)::

		cnx = midi.Connector('path/to/serial/port')::
		cnx.write(msgOut)