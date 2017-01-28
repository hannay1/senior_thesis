import string

class Pword_Analyzer:

	def __init__(self):
		self.cpu_factor = 100
		self.punx = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''


	def get_length(self, password):
		return str(len(password))

	def get_character_counts(self, pasword):
		num_punx = [char in set(string.punctuation) for char in password].count(True)
		arabic_numerals = [char in set(string.digits) for char in password].count(True)
		lowercase_letters = [char in set(string.ascii_lowercase) for char in password].count(True)
		uppercase_letters = [char in set(string.ascii_uppercase) for char in password].count(True)
		return (lowercase_letters, uppercase_letters, arabic_numerals, num_punx)

	def get_base_score(self, password):
		b_s = 0
		arabic_numerals = len(set(string.digits).intersection(password)) > 0
		lowercase_letters = len(set(string.ascii_lowercase).intersection(password)) > 0
		uppercase_letters = len(set(string.ascii_uppercase).intersection(password)) > 0
		punx = len(set(string.punctuation).intersection(password)) > 0
		if arabic_numerals:
			b_s += 10
		elif lowercase_letters:
			b_s += 26
		elif uppercase_letters:
			b_s += 26
			elif punx:
			b_s += 32
			b_s *= len(password)
		return tot



	def get_transitions(self, password):
		char_flag = []
		t_score = 0
		and_space = set(string.punctuation)
		and_space.update(' ')
		#char_flag index --> password char index
		#if key for char_flag i --> True, password character is that type
		for i in range(len(password)):
			if password[i] in set(string.ascii_lowercase):
							char_flag.append(1)
			elif password[i] in set(string.ascii_uppercase):
							char_flag.append(2)
			elif password[i] in set(string.digits):
							char_flag.append(3)
			elif password[i] in and_space:
							char_flag.append(4)
		for i in range(len(password)):	
			if char_flag[i] is not char_flag[i + 1 if i + 1 < len(password) else i]: 
				t_score += 1
			else:
				pass
			return t_score


	def calculate_strength(self, password):

					
