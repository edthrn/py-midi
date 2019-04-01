from .types import (NoteOff, NoteOn, PolyphonicAftertouch,
                    ControlChange, ProgramChange, ChannelAftertouch, PitchBend,
                    SysEx)

TYPES_NUMBER = {
    NoteOff: 0x8, NoteOn: 0x9, PolyphonicAftertouch: 0xa, ControlChange: 0xb,
    ProgramChange: 0xc, ChannelAftertouch: 0xd, PitchBend: 0xe, SysEx: 0xf
}

NUMBERS_TYPE = {v: k for k, v in TYPES_NUMBER.items()}

TYPES_ATTRIBUTES = {
    NoteOff: ['note_number', 'velocity'],
    NoteOn: ['note_number', 'velocity'],
    PolyphonicAftertouch: ['note_number', 'pressure'],
    ControlChange: ['control_number', 'value'],
    ProgramChange: ['program_number'],
    ChannelAftertouch: ['pressure'],
    PitchBend: ['lsbyte', 'msbyte'],
    SysEx: ['manufacturer_id', 'data']
}


class MessageBuilder:
    """An internal object used to build a Message when reading."""
    def __init__(self, status, data1, data2):
        assert 128 <= status <= 255, 'Bad status value.'
        self.status = status
        self.data1 = data1
        self.data2 = data2
        self._message = None

    @property
    def type_number(self):
        return get_message_type_number_from_status(self.status)

    @property
    def channel(self):
        return get_channel_from_status(self.status)

    @property
    def message(self):
        if self._message is None:
            self._message = self._build()
        return self._message

    def _build(self):
        from .midi import Message

        midi_type = NUMBERS_TYPE[self.type_number]
        if self.data2 is not None:
            message_type = midi_type(self.data1, self.data2, internal=True)
        else:
            message_type = midi_type(self.data1, internal=True)

        if isinstance(message_type, NoteOn) and message_type.data2 == 0:
            # NoteOn with velocity = 0 are in fact NoteOff
            message_type = NoteOff(message_type.data1, message_type.data2)

        return Message(message_type, self.channel)


def get_channel_from_status(status):
    """Return the 4 least important bits of status byte.

    According to MIDI standard, channels are numbered from 1 to 16, whereas
    the actual bits go from 0 to 15.
    """
    channel = status & 0xf
    return channel + 1


def get_message_type_number_from_status(status):
    """Return the 4 most important bits of status byte."""
    return status >> 4


def get_status_value(message_type, channel):
    """Return the value of the status byte.

    The first 4 bits represent the message type, the 4 last represent the
    channel.
    """
    type_number = TYPES_NUMBER[message_type]
    first_nibble = type_number << 4
    return first_nibble + channel


def build_message_from_sequence(sequence):
    """Return a MIDI Message object from a sequence of bytes value."""
    sequence = list(sequence)
    assert len(sequence) <= 3, 'Sequence must contain maximum 3 items.'
    builder = MessageBuilder(*sequence)
    return builder.message
