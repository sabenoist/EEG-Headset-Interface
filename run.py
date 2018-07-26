#!/usr/bin/env python2.7
import argparse 
import atexit
import logging
import string
import sys
import threading
import time

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
	elif args.board == "ganglion":
		print ("Board type: OpenBCI Ganglion")
		import openbci.ganglion as bci

	#read physical USB-port
	if "AUTO" == args.port.upper():
		print("Will try do auto-detect board's port. Set it manually with '--port' if it goes wrong.")
		args.port = None
	else:
		print("Port: ", args.port)

	#read notch filtering
	print ("Notch filtering:" + str(args.filtering))

	#read daisy mode
	print ("Daisy mode:" + str(args.daisy))

	#read logging
	if args.log:
		print ("Logging Enabled: log.txt")
		logging.basicConfig(filename="log.txt", format='%(asctime)s - %(levelname)s : %(message)s', level=logging.DEBUG)
		logging.getLogger('yapsy').setLevel(logging.DEBUG)
		logging.info('---------- LOG START ----------')
		logging.info(args)
	else:
		print ("Logging Disabled.")

	init_board(args)


def init_board(args):
	global board

	print ("\n------- INSTANTIATING BOARD -------")
	board = bci.OpenBCIGanglion(port=args.port,
                            daisy=args.daisy,
                            filter_data=args.filtering,
                            scaled_output=True,
                            log=args.log,
                            aux=args.aux)

    #  Info about effective number of channels and sampling rate
	if not board.daisy:
		print (board.getNbEEGChannels(), "EEG channels and", board.getNbAUXChannels(), "AUX channels at", board.getSampleRate(), "Hz.")

	print ("\nBoard ready!")


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="OpenBCI 'user'")
	parser.add_argument('-b', '--board', default="ganglion", 
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
	parser.set_defaults(port="AUTO", filtering=True, log=False, daisy=False, aux=False)

	read_settings(parser.parse_args())
	read_commands()
		
