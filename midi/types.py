# -*-coding:Utf-8 -*

class NoteOff():
	""" Creates a MIDI message type Note Off

	Two positional arguments are required:
	- note number
	- velocity

	"""

	def __init__(self, note_number, velocity):


		if not isinstance(note_number, int) or not isinstance(velocity, int):
			raise TypeError('Note number and pressure value must be type int')
		elif not 0 <= note_number <= 127:
			raise ValueError('Specified note number is out of range. Must be set from 0 to 127 ({} given).'.format(note_number))
		elif not 0 <= velocity <= 127:
			raise ValueError('Specified velocity for note number {} is out of range. Must be set from 0 to 127 ({} given).'.format(note_number, velocity))

		self.note_number = note_number
		self.velocity = velocity

	def __repr__(self):
		return "\nType: Note OFF\nNote number: {}\nVelocity: {}\n".format(self.note_number, self.velocity)

class NoteOn():
	""" Creates a MIDI message type Note On.

	Two positional arguments are required:
	- note number
	- velocity

	 NB: a message type 'Note On' with velocity set to 0 will be read as 'Note Off' on any MIDI device.
	"""

	def __init__(self, note_number, velocity):

		if not isinstance(note_number, int) or not isinstance(velocity, int):
			raise TypeError('Note number and pressure value must be type int')
		elif not 0 <= note_number <= 127:
			raise ValueError('Specified note number is out of range. Must be set from 0 to 127 ({} given).'.format(note_number))
		elif not 0 <= velocity <= 127:
			raise ValueError('Specified velocity for note number {} is out of range. Must be set from 0 to 127 ({} given).'.format(note_number, velocity))

		self.note_number = note_number
		self.velocity = velocity

	def __repr__(self):
		return "\nType: Note ON\nNote number: {}\nVelocity: {}\n".format(self.note_number, self.velocity)

class PolyphonicAftertouch():
	""" Creates a MIDI message type Polyphonic Aftertouch.

	Takes two positional arguments:
	- note number
	- pressure

	NB: this type of message is not so common when reading, because it is expansive to build on a keyboard. It requires
	on sigle sensor per key. Often, Channel Aftertouch is prefered, as it sets a global pressure level for every key.
	"""


	def __init__(self, note_number, pressure):

		if not isinstance(note_number, int) or not isinstance(pressure, int):
			raise TypeError('Note number and pressure value must be type int')
		elif not 0 <= note_number <= 127:
			raise ValueError('Specified note number is out of range. Must be set from 0 to 127 ({} given).'.format(note_number))
		elif not 0 <= pressure <= 127:
			raise ValueError('Specified pressure value for note number {} is out of range. Must be set from 0 to 127 ({} given).'.format(note_number, pressure))

		self.note_number = note_number
		self.pressure = pressure

	def __repr__(self):
		return "\nType: Polyphonic Aftertouch\nNote number: {}\nPressure: {}\n".format(self.note_number, self.pressure)

class ChannelAftertouch():
	""" Creates a MIDI message type Channel Aftertouch.

	Takes one positional argument:
	- pressure value
	"""

	def __init__(self, pressure):

		if not isinstance(pressure, int):
			raise TypeError('Program number must be type int ({} given)'.format(type(pressure)))
		elif not 1 <= pressure <= 128:
			raise ValueError('Specified pressure value is out of range. Must be set from 0 to 127 ({} given).'.format(pressure))

		self.pressure = pressure

	def __repr__(self):
		return "\nType: Channel Aftertouch\nPressure: {}\n".format(self.pressure)

class ControlChange():
	""" Creates a MIDI message type Control Change.

		Takes two positional arguments:
		- control number
		- value
	"""
	def __init__(self, number, value):

		if not isinstance(number, int) or not isinstance(value, int):
			raise TypeError('Control number and value must be type int')
		elif not 0 <= number <= 127:
			raise ValueError('Specified control number is out of range. Must be set from 0 to 127 ({} given).'.format(number))
		elif not 0 <= number <= 127:
			raise ValueError('Specified value for control number {} is out of range. Must be set from 0 to 127 ({} given).'.format(number, value))

		self.control_number = number
		self.value = value

	def __repr__(self):
		return "\nType: Control Change\nControl number: {}\nValue: {}\n".format(self.control_number, self.value)

class ProgramChange():
	""" Creates a MIDI message type Program Change.

	Takes one positional argument:
	- program number
	"""

	def __init__(self, number):

		if not isinstance(number, int):
			raise TypeError('Program number must be type int ({} given)'.format(type(number)))
		elif not 1 <= number <= 128:
			raise ValueError('Specified program number is out of range. Must be set from 1 to 128 ({} given).'.format(number))

		self.program_number = number

	def __repr__(self):
		return "\nType: Program Change\nProgram number: {}\n".format(self.program_number)

class PitchBend():
	"""Creates a MIDI message type Pitch Wheel

	Takes two positional arguments:
	- the least significant byte value (0 to 127)
	- the most significant byte value (0 to 127

	More information about Pitch Bend here :
	https://www.midikits.net/midi_analyser/pitch_bend.htm"""

	def __init__(self, lsbyte, msbyte):

		if not isinstance(lsbyte, int) or not isinstance(msbyte, int):
			raise TypeError('Bytes values must be type int')
		elif not 0 <= lsbyte <= 127:
			raise ValueError('Specified 1st byte value is out of range. Must be set from 0 to 127 ({} given).'.format(lsbyte))
		elif not 0 <= msbyte <= 127:
			raise ValueError('Specified 2nd byte value is out of range. Must be set from 0 to 127 ({} given).'.format(msbyte))

		self.lsbyte = lsbyte
		self.msbyte = msbyte

	def __repr__(self):
		return "\nType: Pitch bend\nLeast signifant byte: {}\nMost significant byte: {}\n".format(self.lsbyte, self.msbyte)

class SysEx():
	"""Creates a MIDI message type SysEx.

	SysEx are used for device-specific data transfer. You can basicaly transfer any data in this type of message.

	The only required argument is the ID (each device manufacturer has its own ID, eg Yamaha (id 43), Roland (id 41) ...)

	Once you specified the ID, you can add as much data as you need to the message.

	Example:
		sysex = SysEx(41, 255, 0, 127, 54) # will build a message specific yo Yamaha devices, with data [255, 0, 127, 54] (in this order)

	*Just give ID and data to arguments, no more, no less.*
	"""

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