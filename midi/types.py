# !/usr/bin/env python3


class MidiMessageType:
    """Parent class to inherit all message types from."""
    def __new__(cls, *args, **kwargs):
        if cls.__name__ == 'MidiMessageType':
            raise RuntimeError('You must instanciate children classes.')
        instance = super().__new__(cls)
        return instance

    def __init__(self, data1, data2=None, internal=False):
        self._internal = internal
        self._type = self.__class__.__name__
        self._build(data1, data2)

        if self._type == 'ProgramChange' and not internal:
            # MIDI standard numbers the PCs from 1 to 128.
            # Therefore, we need to decrement the number in order
            # to have the actual 7 bits value. When the message
            # is built with internal builder – ie from connector.read() –
            # the actual number is already correct.
            assert 1 <= data1 <= 128
            self._data1 = data1 - 1
        else:
            assert 0 <= data1 <= 127
            self._data1 = data1

        if data2 is not None:
            if self._type == 'SysEx':
                assert all(0 <= data <= 255 for data in data2)
            else:
                assert 0 <= data2 <= 127
        self._data2 = data2

    def _build(self, *args):
        from .utils import TYPES_ATTRIBUTES
        for index, attr in enumerate(TYPES_ATTRIBUTES[self.__class__]):
            setattr(self, attr, args[index])

    def __repr__(self):
        name = self.__class__.__name__
        if self._data2 is not None:
            return '{}({}, {})'.format(name, self._data1, self._data2)
        elif name == 'ProgramChange':
            # Increment data_1 to have the MIDI program number, from
            # 1 to 128.
            return '{}({})'.format(name, self._data1 + 1)
        return '{}({})'.format(name, self._data1)

    @property
    def data1(self):
        return self._data1

    @property
    def data2(self):
        return self._data2


class NoteOff(MidiMessageType):
    """MIDI message type Note Off"""


class NoteOn(MidiMessageType):
    """MIDI message type Note On."""


class PolyphonicAftertouch(MidiMessageType):
    """MIDI message type Polyphonic Aftertouch.

    This type of message is not so common when reading, because it is
    expansive to build on a keyboard. It requires on sigle sensor per key.
    Often, Channel Aftertouch is prefered, as it sets a global pressure level
    for every key.
    """


class ChannelAftertouch(MidiMessageType):
    """MIDI message type Channel Aftertouch."""


class ControlChange(MidiMessageType):
    """MIDI message type Control Change."""


class ProgramChange(MidiMessageType):
    """MIDI message type Program Change."""


class PitchBend(MidiMessageType):
    """MIDI message type Pitch Wheel."""


class SysEx(MidiMessageType):
    """MIDI message type SysEx.

    SysEx are used for device-specific data transfer. You can basicaly transfer
    any data in this type of message.

    The only required argument is the ID (each device manufacturer has its own
    ID, eg Yamaha (id 43), Roland (id 41) ...)

    Once you specified the ID, you can add as many data as you need to the
    message.

    Example
    =======
    Build a message specific to Yamaha devices, with data [255, 0, 127, 54]
    (in this order)
    >>> sysex = SysEx(43, 255, 0, 127, 54) 
    """
    def __init__(self, manufacturer_id, *args):
        if not args:
            raise TypeError('Missing data args to build SysEx.')
        self.data = list(args)
        super().__init__(manufacturer_id, self.data)
