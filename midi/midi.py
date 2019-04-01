# !/usr/bin/env python3

from serial import Serial

from .types import SysEx, MidiMessageType
from .utils import (build_message_from_sequence, get_channel_from_status,
                    get_message_type_number_from_status, get_status_value)


class MessageAttribute:
    """A descriptor to access a message attributes directly."""
    def __init__(self, name):
        self.name = name

    def __set__(self, instance, value):
        raise TypeError('"{}" is a read-only attribute.'.format(self.name))

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance.type, self.name)


class Message:
    """A complete MIDI message object.

    Args
    ====
    type (MidiMessageType): see types.py
    channel (int): from 1 to 16. Only if not SysEx message.

    Example:
    >>> from midi.types import NoteOn
    >>> msg = Message(NoteOn(82, 127), 1)

    Attributes:
    - type: the type of message (ControlChange, NoteOn, , ProgramChange, etc...)
    - channel: MIDI channel used for sending/reading messages (from 1 to 16)

    You can also access the attributes of the different message types, eg, for
    ControlChange, you can call
    >>> msg.velocity
    or
    >>> msg.value
    (see help(midi.types) for more details)
    """
    def __init__(self, message_type, channel=0):
        assert isinstance(message_type, MidiMessageType), TypeError(
            'First parameter must be an instance of MidiMessageType.'
        )
        if not isinstance(message_type, SysEx):
            assert 1 <= channel <= 16, \
                "'channel' parameter must be an integer from 1 to 16."
        self.type = message_type
        self.channel = channel
        self._content = None
        self._link_attributes()

    def __repr__(self):
        return "Message({}, channel={})".format(self.type, self.channel)

    def __len__(self):
        return len(self.content)

    def __getitem__(self, index):
        return self.content[index]

    def _get_content(self):
        status = self._get_status_value()
        content = [status, self.type.data1]
        if isinstance(self.type, SysEx):
            content.extend([data for data in self.type.data])
            content.append(0xf7)  # End of SysEx message
        elif self.type.data2 is not None:
            content.append(self.type.data2)

        return content

    def _get_status_value(self):
        """Return the status value of the current message.

        Except for SysEx, the first four bits represent the MIDI message
        type. The last 4 bits represents the channel number, from 0 to 15.
        """
        if isinstance(self.type, SysEx):
            status = 0xf0
        else:
            status = get_status_value(self.type.__class__, self._channel)
        
        return status

    def _link_attributes(self):
        """Link attributes of self.type directly to object.

        This allows, for instance, to access the 'velocity' attribute of a
        NoteOn type message directly from the Message instance itself.
        """
        from .utils import TYPES_ATTRIBUTES
        attributes = {a for attr in TYPES_ATTRIBUTES.values()
                      for a in attr if hasattr(self.type, a)}
        for attr in attributes:
            setattr(self.__class__, attr, MessageAttribute(attr))
    
    @property
    def _channel(self):
        """Internal channel value, from 0 to 15."""
        return self.channel - 1

    @property
    def content(self):
        if self._content is None:
            self._content = self._get_content()
        return self._content

    @property
    def bytes_content(self):
        return [bytes([c]) for c in self.content]

    @property
    def status(self):
        return self.content[0]


class MidiConnector:
    """Interface object between program and machine's serial port.

    Args
    ====
    port (str): path to the machine's serial interface, eg '/dev/serial0'
    on a RaspberryPi3

    baudrate (int): default to 31250, and should not be changed.
    This is the standard baudrate, used by all MIDI devices.

    timeout (float, optional): if you *don't want* the read() method
    to block for ever when waiting for a message, use a timeout to set up a
    maximum duration of blocking. The timeout is only used for reading, not
    writing.
    """
    def __init__(self, port, baudrate=31250, timeout=None, **kwargs):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.__connector = Serial(
            port=self.port, baudrate=self.baudrate, timeout=self.timeout)

        if kwargs.get('test', False):
            # We provide a fake read function when testing
            self.__read_byte = kwargs.get('read_func')
        else:
            self.__read_byte = self.__connector.read

    def __repr__(self):
        return "MidiConnector('{}', baudrate={}, timeout={})".format(
            self.port, self.baudrate, self.timeout)

    def read(self, channel=None):
        """Return a MIDI message from the bytes it reads.

        If 'channel' is specified, return only message(s) received on the given
        channel. Otherwise, read in "omni" mode and return any MIDI message
        received.

        If self.timeout is not None, return nothing if the timeout is reached
        before receiving a message. By default, self.timeout is None, so
        self.read() will block as long as necessary, until receiving a message.
        """
        if channel is None:
            omni = True
        else:
            assert 1 <= channel <= 16, \
                "'channel' parameter must be an integer from 1 to 16."
            omni = False

        msg = [None, None, None]
        sysex = False
        for i in range(len(msg)):
            raw_byte = self.__read_byte()
            if not raw_byte:
                return
            byte_value = ord(raw_byte)
            msg[i] = byte_value
            if msg[1] is not None:
                type_number = get_message_type_number_from_status(msg[0])
                if type_number in (0xc, 0xd):
                    # either a PC message or Channel Aftertouch:
                    # they carry only 2 bytes, not 3
                    break
                elif type_number == 0xf:  # SysEx message
                    sysex = True
                    msg[2] = []
                    while True:
                        raw_byte = self.__read_byte()
                        byte_value = ord(raw_byte)
                        if byte_value != 0xf7:
                            msg[2].append(byte_value)
                        else:  # end of SysEx data
                            break
                    break

        from_channel = get_channel_from_status(msg[0])
        if omni or channel == from_channel or sysex:
            return build_message_from_sequence(msg)

    def write(self, message):
        """Send MIDI message, and return the number of bytes transmitted.

        Args
        ====
        message (midi.Message): message to send via MIDI port.
        """
        assert isinstance(message, Message), TypeError(
            "Argument 'message' must be type Message ({} given).".format(
                (type(message))))

        for byte in message.bytes_content:
            self.__connector.write(byte)

        return len(message)
