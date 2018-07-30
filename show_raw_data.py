import threading
import time
import matplotlib.pyplot as plt


X_AXIS_WIDTH = 1000

#hardware commands
START_STREAMING = 'b'
STOP_STREAMING = 's'


class Print_Raw:
	def __init__(self, board):
		self.board = board

		self.raw_plot1 = plt.subplot(411)
		self.raw_plot2 = plt.subplot(412)
		self.raw_plot3 = plt.subplot(413)
		self.raw_plot4 = plt.subplot(414)

		plt.ion()

	# Multi-threaded version that doesn't work with matplotlib...
	def start_threaded(self):
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


	def start(self):
		self.run_flag = True

		stop_thread = threading.Thread(target=self.__stop)
		stop_thread.daemon = True  # will stop on exit
		
		try:
			stop_thread.start()
		except:
			raise
		
		self.__stream_data()


	def __stop(self):
		raw_input()
		self.run_flag = False


	def __plot_sample(self, sample, x_values, y_values):
		self.raw_plot1.set_xdata(x_values)
		self.raw_plot1.set_ydata(y_values[0])

		self.raw_plot2.set_xdata(x_values)
		self.raw_plot2.set_ydata(y_values[1])

		self.raw_plot3.set_xdata(x_values)
		self.raw_plot3.set_ydata(y_values[2])

		self.raw_plot4.set_xdata(x_values)
		self.raw_plot4.set_ydata(y_values[3])

		plt.draw()


	def __add_y_values(self, y_values, sample, x_counter):
		if x_counter >= X_AXIS_WIDTH:
			y_values[0].pop(0)
			y_values[1].pop(0)
			y_values[2].pop(0)
			y_values[3].pop(0)

		y_values[0].append(sample.channel_data[0])
		y_values[1].append(sample.channel_data[1])
		y_values[2].append(sample.channel_data[2])
		y_values[3].append(sample.channel_data[3])

		return y_values

	def __stream_data(self):
		micro_volts = list()
		micro_volts.append(list())
		micro_volts.append(list())
		micro_volts.append(list())
		micro_volts.append(list())

		x_counter = 0
		x_values = list()

		self.board.ser_write(bytes(START_STREAMING))
		self.board.streaming = True

		while self.run_flag:
			samples = self.__get_samples()

			for sample in samples:
				print "ID: %d\n%s\n" %(int(sample.id), str(sample.channel_data)[1:-1])
				
				micro_volts = self.__add_y_values(micro_volts, sample, x_counter)

				if x_counter < X_AXIS_WIDTH:
					x_values.append(x_counter)
					x_counter += 1

				self.__plot_sample(sample, x_values, micro_volts)

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