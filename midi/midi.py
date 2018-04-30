# -*-coding:Utf-8 -*
from numbers import Number

import serial

from .types import *

class Message:
    """A complete MIDI message object.

    Users must use positional arguments to instantiate:
        1st arg: Type of message (ProgramChange, NoteOff, etc...
            See types.py
        2nd arg: Channel (int from 1 to 16)

    Example:
    >>> msg = Message(NoteOn(82, 127), 1)

    **Users MUST NOT use keywords arguments**. It is implemented for internal
    use only.

    Attributes:
    - type: the type of message (ControlChange, NoteOn, , ProgramChange, etc...)
    - channel: MIDI channel used for sending/reading messages (from 1 to 16)
    - status: the first byte of the message, known as 'status byte'
    - first_data1 and second_data: the second and third bytes
    (if it's a 3-byte message)

    You can also access the attributes of the different message types, eg, for
    ControlChange, you can call
    >>> msg.control_number
    or
    >>> msg.value
    (see types.py for more details)
    """

    def __init__(self, *args, **kwargs):
        self.type = None
        self.channel = None
        self._type = None  # 4 bits reprensenting the message type
        self._status = None  # 1st byte (_type + channel)
        self._data1 = None  # 2nd byte
        self._data2 = None  # 3rd byte

        if kwargs:  # for internal use only (when reading message)
            self._data1 = kwargs['first_data']
            self._data2 = kwargs['second_data']
            self._status = kwargs['status']

            self.channel = (self._status & 15) + 1  # get the 4 least important bits
            self._type = self._status >> 4  # get the 4 most important bits

            if self._type == 8:
                self.type = NoteOff(self._data1, self._data2)
            elif self._type == 9:
                if self._data2 == 0:
                    # NoteOn with velocity = 0 are in fact NoteOff
                    self.type = NoteOff(self._data1, self._data2)
                else:
                    self.type = NoteOn(self._data1, self._data2)
            elif self._type == 10:
                self.type = PolyphonicAftertouch(self._data1, self._data2)
            elif self._type == 11:
                self.type = ControlChange(self._data1, self._data2)
            elif self._type == 12:
                self.type = ProgramChange(self._data1 + 1) # PC are numbered from 1 to 128
            elif self._type == 13:
                self.type = ChannelAftertouch(self._data1)
            elif self._type == 14:
                self.type = PitchBend(self._data1, self._data2)
            elif self._type == 15:
                self.type = SysEx(self._data1, self._data2)
            else:
                raise ValueError(
                    'Status byte must be greater or equal to 128 (1000 0000) '
                    'and less or equal  to 255 (1111 1111)')

        elif args:
            assert len(args) == 2, TypeError(
                "Message.__init__() takes 2 positional arguments: 'type' and "
                "'content' ({} given)".format(len(args)))

            channel = args[1]

            assert isinstance(channel, int), TypeError(
                "2nd positional argument (channel) must be an integer "
                "({} given)".format(type(channel)))
            assert (1 <= channel <= 16), ValueError(
                "2nd argument (channel) is out of range. Must be set from 1 "
                "to 16 ({} given).".format(channel))

            self.channel = channel
            self.type = args[0]
            if isinstance(self.type, NoteOff):
                self._type = 8
                self._data1 = self.type.note_number
                self._data2 = self.type.velocity
            elif isinstance(self.type, NoteOn):
                self._type = 9
                self._data1 = self.type.note_number
                self._data2 = self.type.velocity
            elif isinstance(self.type, PolyphonicAftertouch):
                self._type = 10
                self._data1 = self.type.note_number
                self._data2 = self.type.pressure
            elif isinstance(self.type, ControlChange):
                self._type = 11
                self._data1 = self.type.control_number
                self._data2 = self.type.value
            elif isinstance(self.type, ProgramChange):
                self._type = 12
                self._data1 = self.type.program_number - 1
            elif isinstance(self.type, ChannelAftertouch):
                self._type = 13
                self._data1 = self.type.pressure
            elif isinstance(self.type, PitchBend):
                self._type = 14
                self._data1 = self.type.lsbyte
                self._data2 = self.type.msbyte
            elif isinstance(self.type, SysEx):
                self._type = 15
                self._data1 = self.type.id
                self._data2 = self.type.data
            else:
                raise TypeError(
                    "1st positional argument should be from a type listed "
                    "in types.py (got {} instead)".format(type(self.type)))

            self._status = (self._type << 4) + (self.channel - 1)

        else:
            raise TypeError('__init__() missing 2 required positional arguments:'
                            'type, channel')

    def __repr__(self):
        return "Message({}, {})".format(self.type, self.channel)

    def __len__(self):
        return len(self.content)

    def __getitem__(self, index):
        return self.content[index]

    @property
    def content(self):
        if self._data2 is None:
            return [self._status, self._data1]

        return [self._status, self._data1, self._data2]

    @property
    def velocity(self):
        return self.type.velocity

    @velocity.setter
    def velocity(self, value):
        self.type.velocity = value

    @property
    def pressure(self):
        return self.type.pressure

    @pressure.setter
    def pressure(self, value):
        self.type.pressure = value

    @property
    def value(self):
        return self.type.value

    @value.setter
    def value(self, value):
        self.type.value = value

    @property
    def note_number(self):
        return self.type.note_number

    @note_number.setter
    def note_number(self, value):
        self.type.note_number = value

    @property
    def control_number(self):
        return self.type.control_number

    @control_number.setter
    def control_number(self, value):
        self.type.control_number = value

    @property
    def program_number(self):
        return self.type.program_number

    @program_number.setter
    def program_number(self, value):
        self.type.program_number = value

    @property
    def lsbyte(self):
        return self.type.lsbyte

    @lsbyte.setter
    def lsbyte(self, value):
        self.type.lsbyte = value

    @property
    def msbyte(self):
        return self.type.msbyte

    @msbyte.setter
    def msbyte(self, value):
        self.type.msbyte = value

    @property
    def sysex_id(self):
        return self.type.id

    @sysex_id.setter
    def sysex_id(self, id_):
        self.type.id = id_

    @property
    def sysex_data(self):
        return self.type.data

    @sysex_data.setter
    def sysex_data(self, data):
        self.type.data = data


class MidiConnector:
    """Interface object between program and machine's serial port.

    Args:
    * port (str) – path to the machine's serial interface, eg '/dev/serial0'
    on a RaspberryPi

    * baudrate (int) – default to 31250, and should not be changed.
    This is the standard baudrate, used by all MIDI devices.

    * timeout (float, default to None) – if you *don't want* the read() method
    to block for ever when waiting for a message, use a timeout to set up a
    maximum duration of blocking. The timeout is only used for reading, not
    writing.
    """

    def __init__(self, port, baudrate=31250, timeout=None):
        self.timeout = timeout
        self.baudrate = baudrate
        self.port = port
        self.connector = serial.Serial(
            port=self.port, baudrate=self.baudrate, timeout=self.timeout)

    def __repr__(self):
        return "MidiConnector({}, baudrate={}, timeout={})".format(
            self.port, self.baudrate, self.timeout)

    def read(self, channel=None):
        """
        Return a MIDI message from the bytes it reads.

        If 'channel' is specified, return only message(s) received on the given
        channel. Otherwise, read in "omni" mode and return any MIDI message
        received.

        If self.timeout is not None, return nothing if the timeout is reached
        before receiving a message. By default, self.timeout is None, so
        self.read() will block as long as necessary, until receiving a message.
        """
        sysex = False

        if channel is None:
            omni = True
        else:
            assert isinstance(channel, int), TypeError(
                "Optional argument 'channel' must be an integer "
                "({} given)".format(type(channel[0])))

            assert (1 <= channel <= 16), ValueError(
                "'channel' arg is out of range. Must be set from 1 to 16 "
                "({} given).".format(channel[0]))
            omni = False

        message = [None, None, None]

        for i in range(3):
            data = int.from_bytes(self.connector.read(1), 'big')
            message[i] = data
            if message[1] is not None:
                status = message[0] >> 4
                if status in (12, 13):
                    # either a PC message or Channel Aftertouch:
                    # they carry only 2 bytes, not 3
                    break
                elif status == 15:  # SysEx message
                    sysex = True
                    message[2] = []
                    while True:
                        data = int.from_bytes(self.connector.read(1), 'big')
                        if data != 0xf7:
                            message[2].append(data)
                        else:  # end of SysEx data
                            break
                    break

        if omni or (channel == (message[0] & 15) + 1) or sysex:
            return Message(
                status=message[0],
                first_data=message[1],
                second_data=message[2])
        else:
            pass

    def write(self, message, omni=False):
        """
        Send MIDI message, and return the number of bytes transmitted.

        Args:
            * message (type midi.Message). Contains the information needed to
             build the data bytes to transmit, as well as the channel channel
             to use.
             * omni (bool, default=False) if True, the method will send the
              message to every channels (from 1 to 16), regardless of the
             channel specified inside the Message object.
        """

        assert isinstance(message, Message), TypeError(
            "Argument 'message' must be type Message ({} given).".format(
                (type(message))))

        if message.type != SysEx:
            data1 = bytes([message._data1])
            data2 = bytes([message._data2]) if message._data2 else None
            if not omni:
                status = bytes([message._status])
                msg = [status, data1, data2] if data2 else [status, data1]
                for byte in msg:
                    self.connector.write(byte)
                return len(msg)

            else:  # send MIDI message on every channels
                for i in range(16):
                    status = bytes([(message._type << 4) + i])
                    msg = [status, data1, data2] if data2 else [status, data1]
                    for byte in msg:
                        self.connector.write(byte)
                    return len(msg)

        else:
            start = bytes([0xf0])  # Start of SysEx message
            data1 = bytes([message._data1])  # ID of SysEx
            msg = [start, data1]

            for elmt in message._data2:
                data = bytes([elmt])
                msg.append(data)

            end = bytes([0xf7]) # End of SysEx message
            msg.append(end)
            for byte in msg:
                self.connector.write(byte)
            return len(msg)
