import threading
import time
import matplotlib.pyplot as plt


X_AXIS_WIDTH = 200
CHANNELS = 4 

#hardware commands
START_STREAMING = 'b'
STOP_STREAMING = 's'


class Print_Raw:
	def __init__(self, board):
		self.board = board

		self.fig = plt.figure()

		self.ax1 = self.fig.add_subplot(421)
		plt.ylim(-0.5, 0.5)
		self.ax2 = self.fig.add_subplot(422)
		plt.ylim(-0.5, 0.5)
		self.ax3 = self.fig.add_subplot(423)
		plt.ylim(-0.5, 0.5)
		self.ax4 = self.fig.add_subplot(424)
		plt.ylim(-0.5, 0.5)

		self.raw_plot1, = self.ax1.plot(range(X_AXIS_WIDTH), [0] * X_AXIS_WIDTH)
		self.raw_plot2, = self.ax2.plot(range(X_AXIS_WIDTH), [0] * X_AXIS_WIDTH)
		self.raw_plot3, = self.ax3.plot(range(X_AXIS_WIDTH), [0] * X_AXIS_WIDTH)
		self.raw_plot4, = self.ax4.plot(range(X_AXIS_WIDTH), [0] * X_AXIS_WIDTH)



		plt.ion()
		plt.show()

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


	def __plot_sample(self, y_values):
		self.raw_plot1.set_ydata(y_values[0])
		self.raw_plot2.set_ydata(y_values[1])
		self.raw_plot3.set_ydata(y_values[2])
		self.raw_plot4.set_ydata(y_values[3])

		self.fig.canvas.draw()


	def __animate_y_values(self, y_values, sample,):
		for i in range(CHANNELS):
			y_values[i].pop(0)
			y_values[i].append(sample.channel_data[i])

		return y_values


	def __stream_data(self):
		micro_volts = list()

		for i in range(CHANNELS):
			micro_volts.append([0] * X_AXIS_WIDTH)

		self.board.ser_write(bytes(START_STREAMING))
		self.board.streaming = True

		while self.run_flag:
			samples = self.__get_samples()

			for sample in samples:
				print "ID: %d\n%s\n" %(int(sample.id), str(sample.channel_data)[1:-1])
				
				micro_volts = self.__animate_y_values(micro_volts, sample)

				self.__plot_sample(micro_volts)

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