from status import StatusCheck
from monitor import Monitor
import argparse
import signal
import sys

def sigint_handler(signal, frame):
    print('Exiting!')
    sys.exit(0)
signal.signal(signal.SIGINT, sigint_handler)

def main():
    parser = argparse.ArgumentParser(description='Description of your program')
    
    target_opts = parser.add_argument_group('Target Options', 'Options concerning the target host')
    target_opts.add_argument('-t', '--target', action='store', dest='host', default='', help='Target host to check.')
    target_opts.add_argument('-i', '--interval', action='store', dest='interval', default=60, help='The interval in seconds to check host.')
    
    mode_opts = parser.add_argument_group('Mode Options', 'Choose a mode in which to run')
    mode_opts.add_argument('--status', action='store_true', dest='status', default=False, help='Perform quick status check.')
    mode_opts.add_argument('--monitor', action='store_true', dest='monitor', default=False, help='Constantly monitor server status')
    
    reporting_opts = parser.add_argument_group('Reporting Options', '')
    reporting_opts.add_argument('--report', action='store', dest='report', default='screen', choices=['screen', 'local', 'email', 'gmail'], help='Controls whether status is printed to screen, stored locally, or emailed.')
    reporting_opts.add_argument('--email', action='store', dest='email', default='', help='Email to which to send reports if reporting is set to email or gmail.')
    reporting_opts.add_argument('--password', action='store', dest='password', default='', help="Gmail password. Required if report is set to 'gmail'.")

    args = parser.parse_args()

    if args.host == '':
        site = input('Domain to check: ')
    else:
        site = args.host

    if args.report == 'gmail' and (args.password == '' or args.email == ''):
        print('You must specify your gmail password and address.')
        sys.exit(1)

    if args.report == 'email' and args.email == '':
        print('You must specify an email address to which to send.')
        sys.exit(1)

    if args.monitor:
        monitor = Monitor(site, args)
        monitor.start()

    if args.status:
        status = StatusCheck(site, args)
        status.start()

if __name__ == '__main__':
    main()
