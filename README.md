# python-server-monitor
A simple program to monitor webserver uptime and report back.

```
~/projects/python-server-monitor# python3 main.py -h
Usage: main.py [options]
example: python3 main.py --status
example: python3 main.py --monitor
Control-c to quit.

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit

  Target Options:
    Options concerning the target host

    -t HOST, --target=HOST
                        Target host to check.
    -i INTERVAL, --interval=INTERVAL
                        The interval in seconds to check host.

  Mode Options:
    Choose a mode in which to run

    --status            Perform quick status check.
    --monitor           Constantly monitor server status

  Reporting Options:
    -r REPORT, --report=REPORT
                        Controls whether status is printed to screen, stored
                        locally, or emailed. (Can be 'screen', 'local',
                        'email', or 'gmail')
    -e EMAIL, --email=EMAIL
                        Email to which to send reports if reporting is set to
                        email or gmail.
    -p PASSWORD, --password=PASSWORD
                        Gmail password. Required if report is set to 'gmail'.
```
