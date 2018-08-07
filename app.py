import atexit
import sys
import threading
import time
import pandas as pd
import openbci.ganglion as bci

from pandas_highcharts.core import serialize
from flask import Flask
from flask_cors import CORS


X_AXIS_WIDTH = 200

#hardware commands
START_STREAMING = 'b'
STOP_STREAMING = 's'

app = Flask(__name__)
CORS(app)

micro_volts = list()

for i in range(4):
	micro_volts.append([0] * X_AXIS_WIDTH)


@app.route("/channel1")
def get_channel1():
	channel1_df = pd.DataFrame({'col':micro_volts[0]})
	return serialize(channel1_df, render_to='channel1', output_type='json')


@app.route("/channel2")
def get_channel2():
	channel2_df = pd.DataFrame({'col':micro_volts[1]})
	return serialize(channel2_df, render_to='channel2', output_type='json')


@app.route("/channel3")
def get_channel3():
	channel3_df = pd.DataFrame({'col':micro_volts[2]})
	return serialize(channel3_df, render_to='channel3', output_type='json')


@app.route("/channel4")
def get_channel4():
	channel4_df = pd.DataFrame({'col':micro_volts[3]})
	return serialize(channel4_df, render_to='channel4', output_type='json')


@app.route("/start_streaming")
def start_streaming():
	global run_flag
	run_flag = True
	
	stream_thread = threading.Thread(target=stream_data)
	stream_thread.daemon = True  # will stop on exit
		
	try:
		stream_thread.start()
	except:
		raise

	return "started"

	
@app.route("/stop_streaming")
def stop_streaming():
	global run_flag
	run_flag = False

	return "stopped"


def stream_data():
	global board, run_flag

	board.ser_write(bytes(START_STREAMING))
	board.streaming = True

	while run_flag:
		samples = get_samples()

		for sample in samples:
			print "ID: %d\n%s\n" %(int(sample.id), str(sample.channel_data)[1:-1])

			for i in range(4):
				micro_volts[i].pop(0)
				micro_volts[i].append(sample.channel_data[i])

	board.ser_write(bytes(STOP_STREAMING))
	board.streaming = False


def get_samples():
	global board
	# should the board get disconnected and we could not wait for notification anymore, a reco should be attempted through timeout mechanism
	try:
		board.waitForNotifications(1./board.getSampleRate())
	except Exception as e:
		print("Something went wrong while waiting for a new sample: " + str(e))

	# retrieve current samples on the stack
	samples = board.delegate.getSamples()
	
	return samples


def init_board():
	global board

	print ("\n------- INSTANTIATING BOARD -------")
	try:
		board = bci.OpenBCIGanglion(port=None,
								daisy=False,
								filter_data=False,
								scaled_output=True,
								log=False,
								aux=False)
	except OSError as error:
		print ("\nError: Cannot find OpenBCI Ganglion board. Make sure the board is turned on and that you're root.")
		quit()

	#  Info about effective number of channels and sampling rate
	print board.getNbEEGChannels(), "EEG channels and", board.getNbAUXChannels(), "AUX channels at", board.getSampleRate(), "Hz."

	print ("\nBoard ready!\n")


if __name__ == '__main__':
	init_board()
	app.run()