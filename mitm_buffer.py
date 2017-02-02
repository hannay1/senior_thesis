import mitmproxy, sqlite3, os, base64, sys, random, string
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from get_pwords import *
from pword_analysis import *

class MITM_Interface:

	def __init__(self, uid):
		self.dbName = "Loot.db"
		self.connex = sqlite3.connect(self.dbName)
		self.connex.text_factory = str
		self.cur = self.connex.cursor()
		self.current_user = uid
		self.backend = default_backend()
		self.analyzer = Pword_Analyzer()
		self.initTableA()
		self.initTableB()
		self.initTableS()

	#hashmaps for use when sending to control pannel
	def tableA_vals(self, user_id, pword_id, associated_account, password_length, strength):
		return {"user_id" : user_id,
		"pword_id" : pword_id,
		"associated_account" : associated_account,
		"password_length" : password_length,
		"strength" : strength}

	def tableB_vals(self,user_id, password_id, number_shared_passwords, accounts):
		return {"user_id" : user_id,
		"password_id" : password_id,
		"number_shared_passwords" : number_shared_passwords,
		"accounts" : accounts}

	def assign_strength(self, password):
		return self.analyzer.score_password(password)


	def read_traffic(self, account, password):
		print "mitm_buffer.py uid: " + self.current_user
		p_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(12))
		strength = str(self.assign_strength(password))
		length = str(len(password))
		self.insert_into_table_S(self.current_user, account, password)
		number_shared_passwords = self.get_user_pwords_accounts(self.current_user)
		associated_accounts = number_shared_passwords["accounts"]
		num_passwords =  number_shared_passwords['number_shared_passwords']
		password_id = number_shared_passwords['password_id']
		self.insert_into_table_A(self.current_user, p_id, account, length, strength)
		self.insert_into_table_B(self.current_user, password_id, num_passwords, associated_accounts)
		pass


	def initTableA(self):
		try:
			query = 'CREATE TABLE IF NOT EXISTS TableA' \
					'(user_id TEXT NOT NULL,' \
					'pword_id TEXT UNIQUE NOT NULL,' \
					'associated_account TEXT NOT NULL,' \
					'password_length TEXT NOT NULL,' \
					'strength TEXT NOT NULL)'
			self.cur.execute(query)
			self.connex.commit()
		except sqlite3.Error as SQE:
			print("error inserting record:", SQE)
			pass

	def initTableB(self):
		try:
			query = 'CREATE TABLE IF NOT EXISTS TableB' \
					'(user_id TEXT PRIMARY KEY NOT NULL,' \
					'password_id TEXT NOT NULL,' \
					'number_shared_passwords INTEGER NOT NULL,' \
					'shared_accounts TEXT NOT NULL)'
			self.cur.execute(query)
			self.connex.commit()
		except sqlite3.Error as SQE:
			print("error updating record:", SQE)
			pass


	def initTableS(self):
		try:
			query = 'CREATE TABLE IF NOT EXISTS TableS' \
					'(user_id TEXT NOT NULL,' \
					'associated_account TEXT NOT NULL,' \
					'password BLOB NOT NULL)'
			self.cur.execute(query)
			self.connex.commit()
		except sqlite3.Error as SQE:
			print("error inserting record:", SQE)
			pass
#Fzh6zn6R




	def get_user_pwords_accounts(self, u_id):
		paswds = []
		try:
			self.cur.execute("SELECT DISTINCT password from TableS WHERE user_id = (?)", [u_id])
			passwords = self.cur.fetchall()
			i = 0
			for row in passwords:
				i+=1
				self.cur.execute("SELECT COUNT(password) FROM TableS WHERE password = (?) and user_id = (?)", [row[0], u_id] )
				counts = self.cur.fetchall()
				count = counts[0][0]
				self.cur.execute("SELECT associated_account FROM TableS WHERE password = (?) and user_id = (?)", [row[0], u_id] )
				accounts = self.cur.fetchall()
				account_list = self.get_words(accounts)
				print "password #" + str(i) + " : " + str(count) + " accounts:" + str(accounts)
				paswds.append(("Password # " + str(i), count, account_list))
			vals = self.tableB_vals(self.current_user, paswds[0][0], paswds[0][1], paswds[0][2])
			return vals
		except sqlite3.Error as SQE:
			print("error updating record:", SQE)
			return None


	def insert_into_table_A(self, user_id, pword_id, associated_account, password_length, strength):
		try:
			print("adding to table a...")
			self.cur.execute("INSERT INTO TableA VALUES (?,?,?,?,?)", [user_id, pword_id, associated_account, password_length, strength])
			self.connex.commit()
		except sqlite3.Error as SQE:
			print("error inserting record:", SQE)
			pass

	def insert_into_table_B(self, user_id, password_id, number_shared_passwords, shared_accounts):
		try:
			print("adding to table b...")
			self.cur.execute("INSERT or REPLACE INTO TableB VALUES (?,?,?,?)", [user_id, password_id, number_shared_passwords, shared_accounts])
			self.connex.commit()
			print("successfully inserted records into tables... BBBBBBBB")
		except sqlite3.Error as SQE:
			print("error inserting record:", SQE)
			pass


	def insert_into_table_S(self, user_id, associated_account, password):
		password = self.hash_pword(password)
		password = base64.b64encode(password)
		table_s = str(user_id)
		try:
			print("adding into secure table...")
			self.cur.execute("INSERT INTO TableS VALUES (?, ?, ?)", [user_id, associated_account, password])
			self.connex.commit()
			print("successfully inserted records into tables...")
		except sqlite3.Error as SQE:
			print("error inserting record:", SQE)
			pass



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



	def hash_pword(self, password):
		pword_bytes = password.encode()
		digest = hashes.Hash(hashes.SHA256(), backend=self.backend)
		digest.update(pword_bytes)
		final = digest.finalize()
		return final
