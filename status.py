import logging
import asyncio
import requests
import ssl
from concurrent.futures import ThreadPoolExecutor

class StatusCheck:
    def __init__(self, site, opts):
        self.site = site
        self.opts = opts
        self.logger = logging.getLogger(__name__)
    
    async def run(self):
        with ThreadPoolExecutor() as executor:
            loop = asyncio.get_event_loop()
            tasks = [
                loop.run_in_executor(executor, self.site_running),
                loop.run_in_executor(executor, self.ssl_running),
            ]
            results = await asyncio.gather(*tasks)
            data = {'http': results[0], 'https': results[1]}
            self.logger.info(f'Status for {self.site}: {data}')
            self.report(data)
    
    def report(self, data):
        if self.opts.report == 'screen':
            print(data)
        elif self.opts.report == 'local':
            with open('monitor.log', 'a') as f:
                f.write(json.dumps(data))
        else:
            self.send_email(data)
    
    def send_email(self, data):
        # use Mailer class to send email
        pass
    
    def site_running(self):
        try:
            response = requests.head(f'http://{self.site}')
            return response.status_code < 400
        except Exception as e:
            self.logger.exception(f'Error checking http://{self.site}: {e}')
            return False
    
    def ssl_running(self):
        try:
            with socket.create_connection((self.site, 443)) as sock:
                context = ssl.create_default_context()
                with context.wrap_socket(sock, server_hostname=self.site) as ssock:
                    return True
        except Exception as e:
            self.logger.exception(f'Error checking https://{self.site}: {e}')
            return False
