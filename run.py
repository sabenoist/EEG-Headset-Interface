#!/usr/bin/env python2.7
import argparse 
import atexit
import logging
import string
import sys
import threading
import time
import openbci.ganglion as bci

from yapsy.PluginManager import PluginManager

logging.basicConfig(level=logging.ERROR)

def read_commands():
	global board

	while True:
		cmd = str(raw_input("> "))

		if cmd == "exit" or cmd =="quit":
			board.disconnect()
			quit()
		else:
			print ("  Error: unknown command")


def read_settings(args):
	print ("\n---------- SETTINGS ----------")

	#read board-type
	if args.board == "cyton":
		print ("Board type: OpenBCI Cyton (v3 API)")
		from openbci import cyton as bci
	else:
		print ("Board type: OpenBCI Ganglion")

	#read physical USB-port
	if "AUTO" == args.port.upper():
		print("Port: Auto-detect")
		args.port = None
	else:
		print("Port: ", args.port)

	#read notch filtering
	print ("Notch filtering: " + str(args.filtering))

	#read daisy mode
	print ("Daisy mode: " + str(args.daisy))

	#read logging
	if args.log:
		print ("Logging: Enabled > log.txt")

		logging.basicConfig(filename="log.txt", format='%(asctime)s - %(levelname)s : %(message)s', level=logging.DEBUG)
		logging.getLogger('yapsy').setLevel(logging.DEBUG)
		logging.info('---------- LOG START ----------')
		logging.info(args)
	else:
		print ("Logging: Disabled")

	init_board(args)


def init_board(args):
	global board

	print ("\n------- INSTANTIATING BOARD -------")
	try:
		board = bci.OpenBCIGanglion(port=args.port,
	                            daisy=args.daisy,
	                            filter_data=args.filtering,
	                            scaled_output=True,
	                            log=args.log,
	                            aux=args.aux)
	except OSError as error:
		print ("\nError: Cannot find OpenBCI Ganglion / Cyton board. Make sure the board is turned on and that you're root.")
		quit()

    #  Info about effective number of channels and sampling rate
	if not board.daisy:
		print (board.getNbEEGChannels(), "EEG channels and", board.getNbAUXChannels(), "AUX channels at", board.getSampleRate(), "Hz.")

	print ("\nBoard ready!")


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="OpenBCI 'user'")
	parser.add_argument('-b', '--board',
	                    help="Choose between [cyton] and [ganglion] boards.")
	parser.add_argument('-p', '--port',
	                    help="For Cyton, port to connect to OpenBCI Dongle " +
	                    "( ex /dev/ttyUSB0 or /dev/tty.usbserial-* ). For Ganglion, MAC address of the board. For both, AUTO to attempt auto-detection.")
	parser.add_argument('-n', '--no-filtering', dest='filtering',
	                    action='store_false',
	                    help="Disable notch filtering")
	parser.add_argument('-d', '--daisy', dest='daisy',
	                    action='store_true',
	                    help="Force daisy mode (cyton board)")
	parser.add_argument('-x', '--aux', dest='aux',
	                    action='store_true',
	                    help="Enable accelerometer/AUX data (ganglion board)")
	parser.add_argument('-l', '--log', dest='log', action='store_true',
	                    help="Log program")
	parser.set_defaults(board='ganglion', port="AUTO", filtering=True, log=False, daisy=False, aux=False)

	read_settings(parser.parse_args())
	read_commands()
		
