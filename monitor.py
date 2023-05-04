from status import StatusCheck
import threading

class Monitor():
    def __init__(self, site, opts):
        self.site = site
        self.opts = opts
        self.interval = opts.interval
        self.running = False
        self.timer = None
    
    def run(self):
        if self.running:
            status = StatusCheck(self.site, self.opts)
            status.start()
            self.timer = threading.Timer(self.interval, self.run)
            self.timer.start()
    
    def start(self):
        self.running = True
        self.run()
    
    def stop(self):
        self.running = False
        if self.timer:
            self.timer.cancel()
