from status import StatusCheck
from monitor import Monitor
from optparse import OptionParser, OptionGroup
import signal
import sys

def sigint_handler(signal, frame):
	print('Exiting!')
	sys.exit(0)
signal.signal(signal.SIGINT, sigint_handler)

def main():
	parser = OptionParser(usage='%prog [options]\r\nexample: python3 %prog --status\r\nexample: python3 %prog --monitor\r\nControl-c to quit.', version="%prog 0.1")
	
	targetOpts = OptionGroup(parser, "Target Options", "Options concerning the target host")
	targetOpts.add_option('-t', '--target', action='store', dest='host', default='', help="Target host to check.")
	targetOpts.add_option('-i', '--interval', action='store', dest='interval', default=60, help="The interval in seconds to check host.")
	parser.add_option_group(targetOpts)
	
	modeOpts = OptionGroup(parser, "Mode Options", "Choose a mode in which to run")
	modeOpts.add_option("", "--status", action="store_true", dest="status", default=False, help="Perform quick status check.")
	modeOpts.add_option("", "--monitor", action="store_true", dest="monitor", default=False, help="Constantly monitor server status")
	parser.add_option_group(modeOpts)
	
	reportingOpts = OptionGroup(parser, "Reporting Options", "")
	reportingOpts.add_option("-r", "--report", action='store', dest='report', default='screen', help="Controls whether status is printed to screen, stored locally, or emailed. (Can be 'screen', 'local', 'email', or 'gmail')")
	reportingOpts.add_option("-e", "--email", action='store', dest='email', default='', help="Email to which to send reports if reporting is set to email or gmail.")
	reportingOpts.add_option('-p', '--password', action='store', dest='password', default='', help="Gmail password. Required if report is set to 'gmail'.")
	parser.add_option_group(reportingOpts)
	
	options, args = parser.parse_args()

	if options.host == '':
		site = input('Domain to check: ')
	else:
		site = options.host
	
	if options.report is 'gmail':
		if options.password is '':
			print("You must specify your gmail password.")
			exit(1)
		
		if options.email is '':
			print("You must specify your gmail address.")
			exit(1)
	
	if options.report is 'email':
		if options.email is '':
			print("You must specify an email address to which to send.")
			exit(1)
	
	if options.monitor:
		monitor = Monitor(site, options)
		monitor.start()
	
	if options.status:
		status = StatusCheck(site, options)
		status.start()

if __name__ == "__main__":
	main()