import mitmproxy, sqlite3, os, base64, sys, random, string
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from get_pwords import *
from pword_analysis import *
from password_db_router import *

class MITM_Interface:

	def __init__(self, uid):
		self.current_user = uid
		self.pw_db_router = Password_DB_Router(uid)
		self.p_analyzer = Pword_Analyzer()
		self.backend = default_backend()
		print "starting mitm interface..."

	def assign_strength(self, password):
		return self.p_analyzer.score_password(password)

	def read_traffic(self, account, password):
		print "mitm_buffer.py uid: " + self.current_user
		p_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(12))
		tup = self.assign_strength(password)
		strength = tup[0]
		edit_count = tup[1]
		transitions = tup[2]
		length = str(len(password))
		print "password:" + str(password)
		self.pw_db_router.insert_into_table_A(self.current_user, p_id, account, length, strength, edit_count, transitions, base64.b64encode(self.hash_pword(password)))
		number_shared_passwords = self.pw_db_router.get_user_pwords_accounts(self.current_user, p_id)
		associated_accounts = number_shared_passwords["accounts"]
		num_passwords =  number_shared_passwords['number_shared_passwords']
		password_id = number_shared_passwords['password_id']
		self.pw_db_router.insert_into_table_B(self.current_user, p_id, num_passwords, associated_accounts)
		pass

	def hash_pword(self, password):
		pword_bytes = password.encode()
		digest = hashes.Hash(hashes.SHA256(), backend=self.backend)
		digest.update(pword_bytes)
		final = digest.finalize()
		return final
