import threading
import time
import pandas as pd

from pandas_highcharts.core import serialize
from pandas.compat import StringIO


X_AXIS_WIDTH = 200

#hardware commands
START_STREAMING = 'b'
STOP_STREAMING = 's'


class Print_Raw:
	def __init__(self, board, channels):
		self.board = board
		self.channels = channels


	def start(self):
		self.run_flag = True

		stop_thread = threading.Thread(target=self.stop)
		stop_thread.daemon = True  # will stop on exit
		
		try:
			stop_thread.start()
		except:
			raise
		
		self.stream_data()


	def stop(self):
		raw_input()
		self.run_flag = False


	def stream_data(self):
		micro_volts = list()

		for i in range(CHANNELS):
			micro_volts.append([0] * X_AXIS_WIDTH)

		self.board.ser_write(bytes(START_STREAMING))
		self.board.streaming = True

		while self.run_flag:
			samples = self.get_samples()

			for sample in samples:
				print "ID: %d\n%s\n" %(int(sample.id), str(sample.channel_data)[1:-1])

		self.board.ser_write(bytes(STOP_STREAMING))
		self.board.streaming = False


	def get_samples(self):
		# should the board get disconnected and we could not wait for notification anymore, a reco should be attempted through timeout mechanism
		try:
			self.board.waitForNotifications(1./self.board.getSampleRate())
		except Exception as e:
			print("Something went wrong while waiting for a new sample: " + str(e))

		# retrieve current samples on the stack
		samples = self.board.delegate.getSamples()
		
		#check connection
		#self.board.packets_dropped = self.board.delegate.getMaxPacketsDropped()
		#self.board.check_connection()

		return samples