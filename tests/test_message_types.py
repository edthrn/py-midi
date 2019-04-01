import pytest

from midi.types import (NoteOff, NoteOn, PolyphonicAftertouch,
                        ControlChange, ChannelAftertouch, ProgramChange,
                        PitchBend, SysEx, MidiMessageType)


@pytest.fixture
def note_off():
    return NoteOff(10, 120)


@pytest.fixture
def note_on():
    return NoteOn(20, 110)


@pytest.fixture
def polyphonic_aftertouch():
    return PolyphonicAftertouch(30, 50)


@pytest.fixture
def control_change():
    return ControlChange(72, 40)


@pytest.fixture
def channel_aftertouch():
    return ChannelAftertouch(90)


@pytest.fixture
def program_change():
    return ProgramChange(1)


@pytest.fixture
def pitch_bend():
    return PitchBend(127, 64)


@pytest.fixture
def sysex():
    return SysEx(35, 120, 255, 90)


def test_note_off(note_off):
    assert isinstance(note_off, MidiMessageType)
    assert note_off.data1 == note_off.note_number == 10
    assert note_off.data2 == note_off.velocity == 120
    assert not hasattr(note_off, 'value')


def test_note_on(note_on):
    assert isinstance(note_on, MidiMessageType)
    assert note_on.data1 == note_on.note_number == 20
    assert note_on.data2 == note_on.velocity == 110
    assert not hasattr(note_on, 'value')


def test_polyphonic_aftertouch(polyphonic_aftertouch):
    assert isinstance(polyphonic_aftertouch, MidiMessageType)
    assert polyphonic_aftertouch.data1 == polyphonic_aftertouch.note_number == 30
    assert polyphonic_aftertouch.data2 == polyphonic_aftertouch.pressure == 50
    assert not hasattr(note_on, 'value')


def test_control_change(control_change):
    assert isinstance(control_change, MidiMessageType)
    assert control_change.data1 == control_change.control_number == 72
    assert control_change.data2 == control_change.value == 40
    assert not hasattr(control_change, 'velocity')


def test_channel_aftertouch(channel_aftertouch):
    assert isinstance(channel_aftertouch, MidiMessageType)
    assert channel_aftertouch.data1 == channel_aftertouch.pressure == 90
    assert channel_aftertouch.data2 is None


def test_program_change(program_change):
    assert isinstance(program_change, MidiMessageType)
    assert program_change.data1 == 0  # program_number - 1
    assert program_change.data2 is None
    assert program_change.program_number == 1


def test_pitch_bend(pitch_bend):
    assert isinstance(pitch_bend, MidiMessageType)
    assert pitch_bend.data1 == pitch_bend.lsbyte == 127
    assert pitch_bend.data2 == pitch_bend.msbyte == 64


def test_sysex(sysex):
    assert isinstance(sysex, MidiMessageType)
    assert sysex.data1 == sysex.manufacturer_id == 35
    assert sysex.data2 == [120, 255, 90]