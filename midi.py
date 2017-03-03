import serial
from midiTypeMessage import *
		
class Message():
	"""This class represent a complete MIDI message.

	Attributes:
	- type: the type of message (ControlChange, NoteOn, NoteOff, ProgramChange, etc...)
	- channel: the channel used for sending the message, or for receiving it.

	It has no other available methods than __init__. For building a MIDI message, there are two solutions,
	but one of them (passing keywords parameters) must be used only by the package, when reading MIDI IN messages.

	kwargs when MIDI IN, args when MIDI OUT"""

	def __init__(self, *args, **kwargs):
		"""
		Build the MIDI message.
		
		Warning: keywords arguments *MUST ONLY BE USED* by the package, *NOT* by programmers. 
		
		Programmers using this constructor must use positional arguments.
		Positionnal arguments must be:
			1) Type of message (ProgramChange, NoteOff, etc...). See midiTypeMessages.py
			2) Channel (int from 1 to 16). 

		Be prepared to raise TypeError if you don't respect this order or the required types, or if you want
		to name the arguments.

		Examples: 
		* msg = Message(NoteOff(52, 8), 15) # This is good. It works
		* Passing any other type of arguments will raise a TypeError
		* Passing (25) as 2nd arg (channel) will raise a ValueError (channels go from 1 to 16)
		* msg = Message(channel=15, type=NoteOff(52,8)) # This will also raise a TypeError (unknown keywords argument)
		"""

		self.type = None
		self.channel = None
		self._type = None # 4 bits reprensenting the message type
		self._status = None # 1st byte (_type + channel)
		self._data1 = None # 2nd byte
		self._data2 = None # 3rd byte

		if kwargs:
			for key in kwargs.keys():
				if key not in ['status_byte', 'data_byte1', 'data_byte2']:
					raise TypeError("{} argument unknown. Keywords arguments must be 'status_byte', 'data_byte1' and"
									"data_byte2".format(key))

			self._data1 = kwargs['data_byte1']
			self._data2 = kwargs['data_byte2']
			self._status = kwargs['status_byte']

			self.channel = (self._status & 15) + 1 # get the 4 least important bits
			self._type = self._status >> 4 # get the 4 most important bits

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
			else:
				raise TypeError('Cannot build a MIDI message. Please verify value of status byte (must be greater or equal'
								'than 128 (1000 0000) and less or equal than 255 (1111 1111)')

		elif args:
			if len(args) != 2:
				raise TypeError('Message.__init__() takes 2 positional arguments ({} given)'.format(len(args)))
			else:
				channel = args[1]
				if not isinstance(channel, int):
					raise TypeError('2nd positional argument (channel) must be an integer ({} given)'.format(str(type(channel))))
				elif 1 <= channel <= 16:
					self.channel = channel
				else:
					raise ValueError('2nd argument (channel) is out of range (must be set from 1 to 16, {} given).'.format(channel))

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
				elif isinstance(self.type, ChannelAftertouch):
					self._type = 11
					self._data1 = self.type.pressure
				elif isinstance(self.type, ControlChange):
					self._type = 12
					self._data1 = self.type.control_number
					self._data2 = self.type.value
				elif isinstance(self.type, ProgramChange):
					self._type = 13
					self._data1 = self.type.program_number
				elif isinstance(self.type, PitchWheel):
					self._type = 14
					self._data1 = self.type.lsbyte
					self._data2 = self.type.msbyte
				else:
					raise TypeError('1st positional argument should not be type {}. Must be NoteOff, NoteOn, PolyphonicAftertouch,'
									' ChanelAftertouch, ControlChange, ProgramChange or PitchWheel'.format(str(type((self.type)))))
				
				self._status = (self._type << 4) + self.channel
			
		else:
			raise TypeError('Missing argument to build a Message object (2 positional arguments required)')


	def __repr__(self):
		return "Channel: {}{}".format(self.channel, self.type)

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

	note_number = property(_get_note_number, _set_note_number)
	velocity = property(_get_velocity, _set_velocity)
	pressure = property(_get_pressure, _set_pressure)
	control_number = property(_get_control_number, _set_control_number)
	program_number = property(_get_program_number, _set_program_number)
	lsbyte = property(_get_lsbyte, _set_lsbyte)
	msbyte = property(_get_msbyte, _set_msbyte)


class MidiConnector():

	def __init__(self, port, baudrate=31250, timeout=None):

		if timeout:
			if not isinstance(timeout,int) or not isinstance(timeout, float)
				raise TypeError('Spcecified timeout must be interger or float ({} given)'.format(type(timeout)))

		self.timeout = timeout
		self.baudrate = baudrate
		self.port = port
		self.connector = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)

	def read(self, *channel):

		if not channel:
			omni = True
		elif not isinstance(channel, int):
			raise TypeError('Optional argument (channel) must be an integer.')
		elif not 1 <= channel <= 16:
			raise ValueError('Specified channel out of range. Must be set from 1 to 16 ({} given).'.format(channel))
		else:
			omni = False

		message = [None, None, None]
		for byte in message:
			data = int.from_bytes(self.connector.read(1), 'big')
			byte = data
			if message[1] is not None:
				status = message[0] >> 4 
				if status == 12 or status == 13: # either a PC message or Channel Aftertouch. They carry only 2 bytes, not 3.
					break

		if omni or channel == message[0] + 1:
			return Message(status_byte=message[0], data_byte1=message[1], data_byte2=message[2])
		else:
			pass
		

	def write(self, message, omni=False):

		if not isinstance(message, Message):
			raise TypeError("Argument 'message' must be type Message ({} given).".format(str(type(message))))

		data1 = bytes([message._data1])
		data2 = bytes([message._data2])

		if not omni:
			status = bytes([message._status])
			msg = [status, data1, data2]
			for byte in msg:
				self.connector.write(byte)

		else: # send MIDI message on every channels
			for i in range(16):
				status = bytes([message._status & i])
				msg = [status, data1, data2]
				for byte in msg:
					self.connector.write(byte)
