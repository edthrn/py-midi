import pytest

from midi.midi import Message
from midi.types import NoteOff, SysEx
from midi.utils import get_status_value


@pytest.fixture
def note_off_msg():
    note_off = NoteOff(10, 100)
    return Message(note_off, 1)


@pytest.fixture
def sysex_msg():
    """A SysEx message with 4 bytes of random data with manufacturer ID #35."""
    sysex = SysEx(35, 0x12, 0xac, 0x9a, 0x8d)
    return Message(sysex)


def test_message_content(note_off_msg):
    assert len(note_off_msg) == 3
    assert note_off_msg[0] == 128  # status byte of NoteOff sent on channel 1
    assert note_off_msg[1] == 10
    assert note_off_msg[2] == 100

    assert note_off_msg.content == [128, 10, 100]
    assert note_off_msg.bytes_content == [bytes([c])
                                          for c in note_off_msg.content]

    assert not hasattr(note_off_msg, 'control_number')
    assert hasattr(note_off_msg, 'note_number')
    assert hasattr(note_off_msg, 'velocity')
    assert note_off_msg.note_number == note_off_msg[1]
    assert note_off_msg.velocity == note_off_msg[2]



def test_sysex_content(sysex_msg):
    assert len(sysex_msg) == 7  # ID + 4 bytes of data + start byte + end byte
    assert sysex_msg[0] == 0xf0  # SysEx start byte
    assert sysex_msg[1] == 35
    assert sysex_msg[-1] == 0xf7  # SysEx end byte
