import serial

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

class Message():
	"""Represent a complete MIDI message.

	Attributes:
	- type: the type of message (ControlChange, NoteOn, NoteOff, ProgramChange, etc...)
	- channel: the channel used for sending the message, or for receiving it.
	- status: the first byte of the message, known as 'status byte'
	- data1 and data2: the second and third bytes(if it's a 3 bytes message)

	You can also access the attributes of the different message types.
	Example:
	- if it's a ControlChange, you can call Message.control_number and Message.value
	- if it's a NoteOn, you can call Message.note_number and Message.velocity
	etc... (see midiTypeMessage for more details)
	"""

	def __init__(self, *args, **kwargs):
		"""
		Build the MIDI message.
		
		Warning: keywords arguments *MUST ONLY BE USED* by the library itself, not by programmers. 
		
		Programmers must use positional arguments.
		Positionnal arguments must be:
			1) Type of message (ProgramChange, NoteOff, etc...). See midiTypeMessages.py
			2) Channel (int from 1 to 16). 

		Be prepared to raise TypeError if you don't respect this order or the required types, or if you want
		to name the arguments!

		Examples: 
		* msg = Message(NoteOff(52, 8), 15) # This is good. It works
		-> Passing any other type of arguments will raise a TypeError
		-> Passing (25) as 2nd arg (channel) will raise a ValueError (channels go from 1 to 16)
		* msg = Message(channel=15, type=NoteOff(52,8)) # This will raise a TypeError (unknown keywords argument)
		"""

		self.type = None
		self.channel = None
		self._type = None  # 4 bits reprensenting the message type
		self._status = None  # 1st byte (_type + channel)
		self._data1 = None  # 2nd byte
		self._data2 = None  # 3rd byte

		if kwargs: # Used by the library to build a message when receiving bytes on MIDI IN
			for key in kwargs.keys():
				if key not in ['status_byte', 'data_byte1', 'data_byte2']:
					raise TypeError("{} argument unknown. Keywords arguments must be 'status_byte', 'data_byte1' and"
									"data_byte2".format(key))

			self._data1 = kwargs['data_byte1']
			self._data2 = kwargs['data_byte2']
			self._status = kwargs['status_byte']

			self.channel = (self._status & 15) + 1  # get the 4 least important bits
			self._type = self._status >> 4  # get the 4 most important bits

			if self._type == 8:
				self.type = NoteOff(self._data1, self._data2)
			elif self._type == 9:
				self.type = NoteOn(self._data1, self._data2) if self._data2 != 0 else NoteOff(self._data1, self._data2)
			elif self._type == 10:
				self.type = PolyphonicAftertouch(self._data1, self._data2)
			elif self._type == 11:
				self.type = ControlChange(self._data1, self._data2)
			elif self._type == 12:
				self.type = ProgramChange(self._data1)
			elif self._type == 13:
				self.type = ChannelAftertouch(self._data1)
			elif self._type == 14:
				self.type = PitchWheel(self._data1, self._data2)
			elif self._type == 15:
				self.type = SysEx(self._data1, self._data2)
			else:
				raise TypeError(
					'Cannot build a MIDI message. Please verify value of status byte (must be greater or equal'
					'than 128 (1000 0000) and less or equal than 255 (1111 1111)')

		elif args: # used by programmers for building a message to send via MIDI OUT
			if len(args) != 2:
				raise TypeError('Message.__init__() takes 2 positional arguments ({} given)'.format(len(args)))
			else:
				channel = args[1]
				if not isinstance(channel, int):
					raise TypeError(
						'2nd positional argument (channel) must be an integer ({} given)'.format(str(type(channel))))
				elif 1 <= channel <= 16:
					self.channel = channel
				else:
					raise ValueError(
						'2nd argument (channel) is out of range (must be set from 1 to 16, {} given).'.format(channel))

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
					self._data1 = self.type.program_number
				elif isinstance(self.type, ChannelAftertouch):
					self._type = 13
					self._data1 = self.type.pressure
				elif isinstance(self.type, PitchWheel):
					self._type = 14
					self._data1 = self.type.lsbyte
					self._data2 = self.type.msbyte
				elif isinstance(self.type, SysEx):
					self._type = 15
					self._data1 = self.type.id
					self._data2 = self.type.data
				else:
					raise TypeError(
						'1st positional argument should not be type {}. Must be NoteOff, NoteOn, PolyphonicAftertouch,'
						' ChanelAftertouch, ControlChange, ProgramChange or PitchWheel'.format(str(type((self.type)))))

				self._status = (self._type << 4) + (self.channel - 1)

		else:
			raise TypeError('Missing argument to build a Message object (2 positional arguments required)')

	def __repr__(self):
		return "Channel: {}{}".format(self.channel, self.type)

	def _get_status(self):
		return self._status

	def _get_data1(self):
		return self._data1

	def _get_data2(self):
		return self._data2

	def _get_velocity(self):
		return self.type.velocity

	def _set_velocity(self, velocity):
		self.type.velocity = velocity

	def _get_pressure(self):
		return self.type.pressure

	def _set_pressure(self, pressure):
		self.type.pressure = pressure

	def _get_value(self):
		return self.type.value

	def _set_value(self, value):
		self.type.value = value

	def _get_note_number(self):
		return self.type.note_number

	def _set_note_number(self, note_number):
		self.type.note_number = note_number

	def _get_control_number(self):
		return self.type.control_number

	def _set_control_number(self, control_number):
		self.type.control_number = control_number

	def _get_program_number(self):
		return self.type.program_number

	def _set_program_number(self, program_number):
		self.type.program_number = program_number

	def _get_lsbyte(self):
		return self.type.lsbyte

	def _set_lsbyte(self, lsbyte):
		self.type.lsbyte = lsbyte

	def _get_msbyte(self):
		return self.type.msbyte

	def _set_msbyte(self, msbyte):
		self.type.msbyte = msbyte

	def _get_sysExId(self):
		return self.type.id

	def _set_sysExId(self, id):
		self.type.id = id

	def _get_data(self):
		return self.type.data

	def _set_data(self, data):
		self.type.data = data

	status = property(_get_status)
	data1 = property(_get_data1)
	data2 = property(_get_data2)
	note_number = property(_get_note_number, _set_note_number)
	velocity = property(_get_velocity, _set_velocity)
	pressure = property(_get_pressure, _set_pressure)
	control_number = property(_get_control_number, _set_control_number)
	program_number = property(_get_program_number, _set_program_number)
	lsbyte = property(_get_lsbyte, _set_lsbyte)
	msbyte = property(_get_msbyte, _set_msbyte)
	sysExId = property(_get_sysExId, _set_sysExId)
	sysExData = property(_get_data, _set_data)


class MidiConnector():
	"""Create an interface between the program and the serial port of the machine."""

	def __init__(self, port, baudrate=31250, timeout=None):
		"""
		``port`` must be string, representing the path used for connecting to the machine's serial interface
		Example: on Raspberry3, the path to serial port is '/dev/serial0'

		``baudrate`` is an int set up at 31250 by default and should not be changed. This is the standard
		baudrate, used by all MIDI devices.

		``timeout`` default=None. If you *don't want* the MidiConnector.read() method to block for ever if it receives
		nothing, use this keyword argument to set up a maximum duration of blocking. The timeout is only used for reading,
		not writing.
		"""

		if timeout and not isinstance(timeout,int):
				raise TypeError('Specified timeout must be integer ({} given)'.format(type(timeout)))

		self.timeout = timeout
		self.baudrate = baudrate
		self.port = port
		self.connector = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)

	def read(self, *channel):
		"""
		Return a MIDI message from the bytes it reads.

		If a channel is specified when calling this method, it will return only the message(s) received on this channel.
		Otherwise, it will read in "omni" mode, returning any MIDI message received.

		If a timeout has been specified during instanciation of MidiConnector object, it will return nothing if the timeout
		is reached before receiving a message. By default, timeout is None, which means that the method will block as long 
		as necessary, until receiving a message.
		"""
		sysEx = False

		if not channel:
			omni = True
		elif len(channel) != 1:
			raise ValueError('Only one optional argument max (channel)')
		elif not isinstance(channel[0], int):
			raise TypeError('Optional argument (channel) must be an integer ({} given)'.format(str(type(channel[0]))))
		elif not 1 <= channel[0] <= 16:
			raise ValueError('Specified channel out of range. Must be set from 1 to 16 ({} given).'.format(channel[0]))
		else:
			omni = False
			channel = channel[0]

		message = [None, None, None]
		for i in range(3):
			data = int.from_bytes(self.connector.read(1), 'big')
			message[i] = data
			if message[1] is not None:
				status = message[0] >> 4
				if status == 12 or status == 13:  # either a PC message or Channel Aftertouch. They carry only 2 bytes, not 3.
					break
				elif status == 15:  # SysEx message
					sysEx = True
					message[2] = []
					while True:
						data = int.from_bytes(self.connector.read(1), 'big')
						if data != 0xf7:
							message[2].append(data)
						else:
							break
					break

		if omni or channel == (message[0] & 15) + 1 or sysEx:
			return Message(status_byte=message[0], data_byte1=message[1], data_byte2=message[2])
		else:
			pass

	def write(self, message, omni=False):
		"""
		Send MIDI message, and return the number of bytes transmitted.

		``message`` must be type midi.Message or will raise a TypeError. This Message object contains the information
		needed to build the bytes and transmit them, and to know on which channel to send the bytes.
		``omni`` (default=False) If set up at True, the method will send the message to every channels (from
		1 to 16), regardless of the channel specified inside the Message object.
		"""
		if not isinstance(message, Message):
			raise TypeError("Argument 'message' must be type Message ({} given).".format(str(type(message))))

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
			start = bytes([0xf0]) # Start of SysEx message
			data1 = bytes([message._data1]) # ID of SysEx
			msg = [start, data1]

			for elmt in message._data2:
				data = bytes([elmt])
				msg.append(data)

			end = bytes([0xf7]) # End of SysEx message
			msg.append(end)
			for byte in msg:
				self.connector.write(byte)
			return len(msg)
