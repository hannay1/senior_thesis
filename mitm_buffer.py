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

	#hashmaps for use when sending to debriefing page
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
		return self.analyzer.score_password(password)

	def check_for_shared_passwords(self, uid):
		try:
			query = 'CREATE TABLE IF NOT EXISTS TableA' \
					'(user_id TEXT PRIMARY KEY NOT NULL,' \
					'pword_id TEXT UNIQUE NOT NULL,' \
					'associated_account TEXT NOT NULL,' \
					'strength INTEGER NOT NULL)'
			self.cur.execute(query)
			self.connex.commit()
		except sqlite3.Error as SQE:
			print("error inserting record:", SQE)
			pass

	def read_traffic(self, account, password):
		print "mitm_buffer.py uid: " + self.current_user
		p_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(12))
		strength = str(self.assign_strength(password))
		length = str(len(password))
		number_shared_passwords = self.get_user_pwords_accounts(self.current_user)
		self.insert_into_table_S(self.current_user, account, password)
		self.insert_into_table_A(self.current_user, p_id, account, length, strength)
		self.insert_into_table_B(self.current_user, number_shared_passwords)
		pass


	def initTableA(self):
		try:
			query = 'CREATE TABLE IF NOT EXISTS TableA' \
					'(user_id TEXT PRIMARY KEY NOT NULL,' \
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
					'number_shared_passwords INTEGER NOT NULL)'
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

	def get_user_pwords_accounts(self, u_id):
		try:
			self.cur.execute("SELECT password, associated_account FROM TableS WHERE user_id = (?)", [u_id])
			self.cur.execute("SELECT password, associated_account, COUNT() FROM TableS WHERE user_id = (?)", [u_id])
			pw_db = self.cur.fetchall()
			for row in pw_db:
				print str(row)
				#get all passwords from account a, b, etc...
			if not pw_db:
				raise sqlite3.Error
			return pw_db
		except sqlite3.Error as SQE:
			print("error updating record:", SQE)
			return None


	def insert_into_table_A(self, user_id, pword_id, associated_account, password_length, strength):
		try:
			print("adding to table a...")
			self.cur.execute("INSERT OR IGNORE INTO TableA VALUES (?,?,?,?,?)", [user_id, pword_id, associated_account, password_length, strength])
			self.connex.commit()
		except sqlite3.Error as SQE:
			print("error inserting record:", SQE)
			pass

	def insert_into_table_B(self, user_id, number_shared_passwords):
		try:
			print("adding to table b...")
			self.cur.execute("INSERT OR IGNORE INTO TableB VALUES (?,?)", [user_id, number_shared_passwords])
			self.connex.commit()
			print("successfully inserted records into tables...")
		except sqlite3.Error as SQE:
			print("error inserting record:", SQE)
			pass


	def insert_into_table_S(self, user_id, associated_account, password):
		password = self.hash_pword(password)
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
