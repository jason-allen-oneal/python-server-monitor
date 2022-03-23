from status import StatusCheck
import sched, time

class Monitor():
	def __init__(self, site, opts):
		self.site = site
		self.opts = opts
		self.interval = opts.interval
		self.running = False
		self.sched = sched.scheduler(time.time, time.sleep)
	
	def run(self):
		if self.running:
			status = StatusCheck(self.site, self.opts)
			status.start()
			self.event = self.sched.enter(self.interval, 1, self.run)
	
	def start(self):
		self.running = True
		self.run()
		self.sched.run()
	
	def stop(self):
		self.running = False
		if self.sched and self.event:
			self.sched.cancel(self.event)