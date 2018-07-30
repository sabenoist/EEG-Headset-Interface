import threading
import time


#hardware commands
START_STREAMING = 'b'
STOP_STREAMING = 's'


class Print_Raw:
	def __init__(self, board):
		self.board = board


	def start(self):
		stream_thread = threading.Thread(target=self.__stream_data)
		stream_thread.daemon = True  # will stop on exit
		self.run_flag = True

		try:
			stream_thread.start()
		except:
			raise

		raw_input()
		self.run_flag = False
		time.sleep(0.2)  # give the thread some time to finish up.


	def __plot_sample(sample):
		#TODO: write this.
		pass


	def __stream_data(self):
		self.board.ser_write(bytes(START_STREAMING))
		self.board.streaming = True

		while self.run_flag:
			samples = self.__get_samples()

			for sample in samples:
				print "ID: %d\n%s\n" %(int(sample.id), str(sample.channel_data)[1:-1])
				self.__plot_sample(sample)

		self.board.ser_write(bytes(STOP_STREAMING))
		self.board.streaming = False


	def __get_samples(self):
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