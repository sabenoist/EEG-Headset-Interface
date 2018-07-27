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
manager = PluginManager()


def read_plugins(args):
	global plug_list, callback_list, board
	plug_list = []
	callback_list = []

	if args.add:
		for plug_candidate in args.add:
			# first value: plugin name, then optional arguments
			plug_name = plug_candidate[0]
			plug_args = plug_candidate[1:]
			# Try to find name
			plug = manager.getPluginByName(plug_name)
			if plug == None:
				# eg: if an import fail inside a plugin, yapsy skip it
				print ("Error: [ " + plug_name + " ] not found or could not be loaded. Check name and requirements.")
			else:
				print ("\nActivating [ " + plug_name + " ] plugin...")
				if not plug.plugin_object.pre_activate(plug_args, sample_rate=board.getSampleRate(), eeg_channels=board.getNbEEGChannels(), aux_channels=board.getNbAUXChannels(), imp_channels=board.getNbImpChannels()):
					print ("Error while activating [ " + plug_name + " ], check output for more info.")
				else:
					print ("Plugin [ " + plug_name + "] added to the list")
					plug_list.append(plug.plugin_object)
					callback_list.append(plug.plugin_object)

	if len(plug_list) == 0:
		callback_list = None


def read_settings(args):
	plugins_paths = ["openbci/plugins"]
	if args.plugins_path:
		plugins_paths += args.plugins_path
	manager.setPluginPlaces(plugins_paths)
	manager.collectPlugins()

	# Print list of available plugins and exit
	if args.list:
		print ("Available plugins:")
		for plugin in manager.getAllPlugins():
			print ("\t- " + plugin.name)
		exit()

	# User wants more info about a plugin
	if args.info:
		plugin = manager.getPluginByName(args.info)
		if plugin == None:
			# eg: if an import fail inside a plugin, yapsy skip it
			print ("Error: [ " +  args.info + " ] not found or could not be loaded. Check name and requirements.")
		else:
			print (plugin.description)
			plugin.plugin_object.show_help()
		exit()

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
		print board.getNbEEGChannels(), "EEG channels and", board.getNbAUXChannels(), "AUX channels at", board.getSampleRate(), "Hz."

	def cleanUp():
		board.disconnect()
		print ("  Deactivating Plugins...")
		for plug in plug_list:
			plug.deactivate()
		print ("  Exiting...")

	atexit.register(cleanUp)

	print ("\nBoard ready!")


def read_commands():
	global board, callback_list

	# Init board state
	# s: stop board streaming; v: soft reset of the 32-bit board (no effect with 8bit board)
	s = 'sv'
	# Tell the board to enable or not daisy module
	if board.daisy:
		s = s + 'C'
	else:
		s = s + 'c'
	# d: Channels settings back to default
	s = s + 'd'

	while (s != "/exit" or s != "/quit"):
		# Send char and wait for registers to set
		if (not s):
			pass

		elif board.streaming and s != "/stop":
			print ("Error: the board is currently streaming data, please type '/stop' before issuing new commands.")
		else:
			# read silently incoming packet if set (used when stream is stopped)
			flush = False

			if ('/' == s[0]):
				s = s[1:]

				if ("T:" in s):
					lapse = int(s[string.find(s, "T:") + 2:])
				elif ("t:" in s):
					lapse = int(s[string.find(s, "t:") + 2:])
				elif ("T:" not in s and "t:" not in s):
					lapse = -1
				elif ('startimp' in s):
					if board.getBoardType() == "cyton":
						print ("Impedance checking not supported on cyton.")
					else:
						board.setImpedance(True)
						if (callback_list != None):
							# start streaming in a separate thread so we could always send commands in here
							boardThread = threading.Thread(target=board.start_streaming, args=(callback_list, lapse))
							boardThread.daemon = True  # will stop on exit
							try:
								boardThread.start()
							except:
								raise
						else:
							print ("No function loaded")
				elif ("start" in s):
					board.setImpedance(False)
					if (callback_list != None):
						# start streaming in a separate thread so we could always send commands in here
						boardThread = threading.Thread(target=board.start_streaming, args=(callback_list, lapse))
						boardThread.daemon = True  # will stop on exit
						try:
							boardThread.start()
						except:
							raise
					else:
						print ("No function loaded")
				elif ('test' in s):
					test = int(s[s.find("test") + 4:])
					board.test_signal(test)
				elif ('stop' in s):
					board.stop()
					flush = True
				else:
					print("  Error: Command not recognized")

			elif s:
				for c in s:
					if sys.hexversion > 0x03000000:
						board.ser_write(bytes(c, 'utf-8'))
					else:
						board.ser_write(bytes(c))
					time.sleep(0.100)

			line = ''
			time.sleep(0.1)  # Wait to see if the board has anything to report
			# The Cyton nicely return incoming packets -- here supposedly messages -- whereas the Ganglion prints incoming ASCII message by itself
			if board.getBoardType() == "cyton":
				while board.ser_inWaiting():
					c = board.ser_read().decode('utf-8',
												errors='replace')  # we're supposed to get UTF8 text, but the board might behave otherwise
					line += c
					time.sleep(0.001)
					if (c == '\n') and not flush:
						print('%\t' + line[:-1])
						line = ''
			elif board.getBoardType() == "ganglion":
				while board.ser_inWaiting():
					board.waitForNotifications(0.001)

			if not flush:
				print(line)

		# Take user input
		# s = input('--> ')
		if sys.hexversion > 0x03000000:
			s = input('\n> ')
		else:
			s = raw_input('\n> ')


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
	parser.add_argument('--log', dest='log', action='store_true',
						help="Log program")
	parser.add_argument('-a', '--add', metavar=('PLUGIN', 'PARAM'),
						action='append', nargs='+',
						help="Select which plugins to activate and set parameters.")
	parser.add_argument('-l', '--list', action='store_true',
						help="List available plugins.")
	parser.add_argument('-i', '--info', metavar='PLUGIN',
						help="Show more information about a plugin.")
	parser.add_argument('--plugins-path', dest='plugins_path', nargs='+',
						help="Additional path(s) to look for plugins")
	parser.set_defaults(board='ganglion', port="AUTO", filtering=True, log=False, daisy=False, aux=False)

	args = parser.parse_args()

	read_settings(args)
	init_board(args)
	read_plugins(args)

	read_commands()
