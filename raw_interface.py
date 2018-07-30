import atexit
import sys
import openbci.ganglion as bci

from print_raw_data import Print_Raw

CMD_WAIT_TIME = 0.100


def read_command():
	global board

	show_cmd_menu()
	
	read_cmd = False
	while not read_cmd:
		cmd = raw_input("\nPick an option: ")

		if cmd == "1":
			program = Print_Raw(board)
		elif cmd == "x":
			quit()
		else:
			print "Error: unknown option."
			continue

		read_cmd = True

		program.start()


def show_cmd_menu():
	print "\n----- MENU -----"
	print "[1]	Print raw data."
	print "[x]	Exit"


def init_board():
	global board

	print ("------- INSTANTIATING BOARD -------")
	try:
		board = bci.OpenBCIGanglion(port=None,
								daisy=False,
								filter_data=False,
								scaled_output=False,
								log=False,
								aux=False)
	except OSError as error:
		print ("\nError: Cannot find OpenBCI Ganglion board. Make sure the board is turned on and that you're root.")
		quit()

	#  Info about effective number of channels and sampling rate
	print board.getNbEEGChannels(), "EEG channels and", board.getNbAUXChannels(), "AUX channels at", board.getSampleRate(), "Hz."

	print ("\nBoard ready!")


if __name__ == '__main__':
	init_board()

	while True:
		read_command()