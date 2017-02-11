import sys, os, time, requests, signal, json
from collections import MutableMapping
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Browser_Parser:


	def __init__(self):
		self.uname = "beef"
		self.pword = "eaterGin308"
		self.cert_key = "/opt/beef/beef_key.pem"
		self.cert_cert = "/opt/beef/beef_cert.pem"
		self.cert = (self.cert_cert, self.cert_key)
		self.api_key = self.get_api_key()

	def get_api_key(self):
		hed = "Content-Type: application/json"
		to_beef_serv = {'username' : self.uname, 'password' : self.pword}
		k_une = requests.post(url="https://192.168.3.1:3000/api/admin/login", cert=self.cert, verify=False, json=to_beef_serv)
		k_dict = json.loads(k_une.text)
		return k_dict['token']

	def is_loggedin_facebook(self):
		#IDEA: modify detect_soc_nets in beef/modules/ to deal with amazon, CC login, etc
		pass

	def is_loggedin_google(self):
		pass

	def is_loggedin_twitter(self):
		pass

	def check_toolbars(self):
		pass

	def check_lastpass(self):
		pass

	def check_popup_blocker(self):
		pass

	def check_adblock(self):
		pass

	def check_antivirus(self):
		pass

	def get_sesh_id(self):
		pass

	def get_browser_deets(self):
		#also gets OS details etc
		pass


if __name__ == "__main__":
	bp = Browser_Parser()
	bp.print_key()