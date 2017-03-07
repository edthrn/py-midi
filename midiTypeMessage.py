#!/usr/bin/python
# -*-coding:Utf-8 -*

class NoteOff():
	def __init__(self, note_number, velocity):
		self.note_number = note_number
		self.velocity = velocity

	def __repr__(self):
		return "\nType: Note OFF\nNote number: {}\nVelocity: {}\n".format(self.note_number, self.velocity)

class NoteOn():
	def __init__(self, note_number, velocity):
		self.note_number = note_number
		self.velocity = velocity

	def __repr__(self):
		return "\nType: Note ON\nNote number: {}\nVelocity: {}\n".format(self.note_number, self.velocity)

class PolyphonicAftertouch():
	def __init__(self, note_number, pressure):
		self.note_number = note_number
		self.pressure = pressure

	def __repr__(self):
		return "\nType: Polyphonic Aftertouch\nNote number: {}\nPressure: {}\n".format(self.note_number, self.pressure)

class ChannelAftertouch():
	def __init__(self, pressure):
		self.pressure = pressure

	def __repr__(self):
		return "\nType: Channel Aftertouch\nPressure: {}\n".format(self.pressure)

class ControlChange():
	def __init__(self, number, value):
		self.control_number = number
		self.value = value

	def __repr__(self):
		return "\nType: Control Change\nControl number: {}\nValue: {}\n".format(self.control_number, self.value)

class ProgramChange():
	def __init__(self, number):
		self.program_number = number

	def __repr__(self):
		return "\nType: Program Change\nProgram number: {}\n".format(self.program_number)

class PitchWheel():
	"""docstring for PitchWheel
	https://www.midikits.net/midi_analyser/pitch_bend.htm"""
	def __init__(self, lsbyte, msbyte):
		self.lsbyte = lsbyte
		self.msbyte = msbyte

	def __repr__(self):
		return "\nType: Pitch wheel\nLeast signifant byte: {}\nMost significant byte: {}\n".format(self.lsbyte, self.msbyte)

class SysEx():
	def __init__(self, id, *args):
		self.id = id
		self.data = []

		if args:
			for arg in args:
				if not isinstance(arg, int):
					raise TypeError('All data transmitted through SysEx must be integers ({} given)'.format(type(arg)))
				else:
					self.data.append(arg)

	def __repr__(self):
		return "\nType: SysEx message\nID: {}\nData: {}\n".format(self.id, self.data)
