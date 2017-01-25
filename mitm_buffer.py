import mitmproxy, sqlite3, os, base64, sys
from get_pwords import Get_Pwords

class MITM_Interface:

	def __init__(self):
		self.dbName = "Loot.db"
		self.connex = sqlite3.connect(self.dbName)
		self.cur = self.connex.cursor()
		self.cpu_factor = 0
		self.new_user = True #replace this with more sophisticated check

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
		'''assigns a password a "strength" value determined by: 
		# of permutations of characters, 
		password length, 
		distribution of unique characters,
		self.cpu_factor (approximate cpu clockspeed)

		--> number of years to crack?
		'''
		return -1

	def new_user_id(self):
		return os.urandom(8) if self.new_user

	def check_for_shared_passwords(self,):
		'''checks traffic for shared passwords'''

		return None

	def read_traffic(self, account, password):
		'''makes decisions based on account names and passwords from mitmproxy : inserts into table(s), makes a new userID, etc'''
		u_id = str(self.new_user_id())
		p_id = str(os.urandom(10))
		pword_length = str(password.length())
		print("password: ", password)
		print("length of password: ", pword_length)
		strength = self.assign_strength(password)
		num_shared = self.check_for_shared_passwords()
		self.insert_into_tables()
		pass

	def initTableA(self):
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

	def initTableS(self, u_id):
		print("creating new secure table..")
		try:
			query = 'CREATE TABLE IF NOT EXISTS Table' + str(u_id) + ' ' +  \
					'(user_id TEXT PRIMARY KEY NOT NULL,' \
					'associated_account TEXT NOT NULL,' \
					'password BLOB NOT NULL)'
			print("table" + str(uid) + " created...")
			self.cur.execute(query)
			self.connex.commit()
		except sqlite3.Error as SQE:
			print("error inserting record:", SQE)
			pass

	def get_user_pword_table(self, u_id):
        try:
        	table_s = str(uid)
            self.cur.execute("SELECT * FROM Table" + table_s + " WHERE username_hash = [?,?,?]", [username_hash, associated_account, password])
            pw_db = self.cur.fetchone()
            if not pw_db:
                raise sqlite3.Error
            print("got enc'd user db")
            return pw_db
        except sqlite3.Error as SQE:
            print("error updating record:", SQE)
            return None


	def insert_into_tables(self, user_id, pword_id, associated_account, password_length, strength, number_shared_passwords, password):
		password = base64.b64encode()
        table_s = str(uid)
		try:
			print("adding to table a...")
			self.cur.execute("INSERT OR IGNORE INTO TableA VALUES (?,?,?,?,?)", [user_id, pword_id, associated_account, password_length, strength])
			self.connex.commit()
			print("adding to table b...")
			self.cur.execute("INSERT OR IGNORE INTO TableB VALUES (?,?)", [user_id, number_shared_passwords])
			self.connex.commit()
			if password is not None:
				print("adding into secure table...")
				self.cur.execute("INSERT INTO Table" + table_s + " VALUES (?, ?)", [user_id, associated_account, password])
				print("successfully inserted records into tables...")
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
            return None


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

