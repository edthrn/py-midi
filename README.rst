py-midi
=======

**Simply send and receive MIDI messages using Python3.**

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY.

**Warning: To use with Python3 only**. The library doesn't work with Python2.

1. Purpose
-----------

This Python3 library has been made in order to communicate easily with any MIDI devices. The only requirement is to have a serial
interface on your machine. It's on this interface that you must connect MIDI cables to establish a communication between your
machine and the MIDI devices.

The py-midi library allows users to build and/or read MIDI messages without having to worry on formating them before sending and/or after receiving.

MIDI (Musical Instrument Digital Interface) is a standard used for making easy for instruments, computers and other electronic devices
to communicate.

This library is able to deal with any kind of MIDI messages, on any of the 16 possible channels (for channel-type messages) or with any kind of SysEx messages.

For more details on the MIDI standard, see Wikipedia MIDI page https://en.wikipedia.org/wiki/MIDI

2. Installation
---------------
Easily install the package using `pip`::

	$ pip3 install py-midi

Then you can import the package to your program:

.. code-block:: python

	>>> import midi


3. Getting started
-------------------

Creates an interface between your program and the serial port of the machine. You instanciate by giving the path to the serial port. Example:

.. code-block:: python

  >>> from midi import MidiConnector
  >>> conn = MidiConnector('/dev/serial0')  # path to use on RaspberryPi 3

If you don't want the ``MidiConnector.read()`` method to block forever if it receives nothing, use the keyword argument **timeout** to set up a maximum duration (seconds) of blocking:

.. code-block:: python

    >>> conn = MidiConnector('/dev/serial0', timeout=5)

The ``timeout`` kwarg is only used for reading, not for writing.

To send a MIDI message, you first need to instantiate a ``MidiMessageType``. There are 8 differents types of MIDI message. Here they are, with there instanciation parameters:

* ``NoteOff(note_number, velocity)``
* ``NoteOn(note_number, velocity)``
* ``PolyphonicAftertouch(note_number, pressure)``
* ``ChannelAftertouch(pressure)``
* ``ControlChange(control_number, value)``
* ``ProgramChange(program_number)``
* ``PitchWheel(lsbyte, msbyte)``
* ``SysEx(manufacturer_id, data1, data2..., dataN)``

**NOTE**
All instanciation parameters must be included within [0, 127] except for ``SysEx`` data (0 to 255) or ``ProgramChange``' number (1 to 128).

Example: create a type ``ControlChange``:

.. code-block:: python

    >>> from midi import ControlChange
    >>> cc = ControlChange(100, 127)

Now build the full message, providing a channel:

.. code-block:: python

    >>> from midi import Message
    >>> msg = Message(cc, channel=1)

You can access the attributes of your message directly:

.. code-block:: python

    >>> msg.control_number
    100
    >>> msg.value
    127

Send the message to MIDI OUT, using the connector:

.. code-block:: python

    >>> conn.write(msg)  # returns the number of bytes sent
    3

-------

For reading messages received via MIDI IN, use the method ``read()`` as follow:

.. code-block:: python

    >>> msg = conn.read()  # read on ANY channel by default
    >>> # Pretend to receive a ProgramChange message, on channel 2
    >>> msg
    Message(ProgramChange(35), 2)
    >>> msg.channel
    2
    >>> msg.type
    ProgramChange(35)
    >>> msg.program_number
    35

By default, the connector's ``read()`` method reads in OMNI mode. To specify a channel, add the channel number as a parameter:

.. code-block:: python

    >>> msg = conn.read(8)  # read only on channel 8, ignore the rest

As per the MIDI standard, there are 16 channels you can read from, numbered from 1 to 16.
