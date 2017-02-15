import mitmproxy, sqlite3, os, base64, sys, random, string

class Browser_DB_Router:

	def __init__(self, uid):
		self.dbName = "Loot2.db"
		self.connex = sqlite3.connect(self.dbName)
		self.connex.text_factory = str
		self.cur = self.connex.cursor()
		self.current_user = uid
		self.backend = default_backend()
		self.initTable()

	def initTable(self):
		try:
			self.cur.execute('CREATE TABLE IF NOT EXISTS BrowserTable' \
					'(user_id TEXT NOT NULL,' \
					'hooked_browser_id TEXT UNIQUE NOT NULL,' \
					'browser_name TEXT NOT NULL,' \
					'browser_version TEXT NOT NULL,' \
					'os TEXT NOT NULL,' \
					'browser_plugins TEXT NOT NULL,'\
					'has_logged_in INTEGER NOT NULL,'\
					'has_clicked INTEGER NOT NULL,'\
					'session_id TEXT NOT NULL,'\
					'recent_login_cmd TEXT NOT NULL,'\
					'recent_toolbar_cmd TEXT NOT NULL)')
			self.connex.commit()
		except sqlite3.Error as SQE:
			print("error initting table:", SQE)
			pass

	def insert_into_BrowserTable(self, user_id, hooked_browser_id, browser_name, browser_version, os, browser_plugins, session_id, login_cmd, toolbar_cmd):
		try:
			print("adding to browser table...")
			self.cur.execute("INSERT or IGNORE INTO BrowserTable VALUES (?,?,?,?,?,?,?,?,?,?,?)", [user_id, hooked_browser_id, browser_name, browser_version, os, browser_plugins, 0, 0, session_id,login_cmd, toolbar_cmd])
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
			self.cur.execute("UPDATE BrowserTable SET has_clicked = ? WHERE user_id = ?", [did_toolbar,user_id])
			self.connex.commit()
			print("successfully inserted records into browser table...")
		except sqlite3.Error as SQE:
			print("error inserting record:", SQE)
			pass

	def update_BrowserTable_Session_id(self, user_id, session_id):
		try:
			print("adding to browser table...")
			self.cur.execute("UPDATE BrowserTable SET session_id = ? WHERE user_id = ?", [session_id, user_id])
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

	def update_BrowserTable_Session_id(self, user_id, toolbar_cmd):
		try:
			print("adding to browser table...")
			self.cur.execute("UPDATE BrowserTable SET recent_toolbar_cmd = ? WHERE user_id = ?", [toolbar_cmd, user_id])
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
			return str(sesh_id)
		except sqlite3.Error as SQE:
			print("error finding record:", SQE)
			pass


