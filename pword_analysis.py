import string

class Pword_Analyzer:

	def __init__(self):
		self.cpu_factor = 100
		self.wordlist = "passwords_john.txt"
		self.punx_set = set(string.punctuation)
		self.punx_set.update(' ')

	def get_length(self, password):
		return len(password)

	def get_character_counts(self, password):
		num_punx = [char in self.punx_set for char in password].count(True)
		arabic_numerals = [char in set(string.digits) for char in password].count(True)
		lowercase_letters = [char in set(string.ascii_lowercase) for char in password].count(True)
		uppercase_letters = [char in set(string.ascii_uppercase) for char in password].count(True)
		return (lowercase_letters, uppercase_letters, arabic_numerals, num_punx)

	def get_base_score(self, password):
		char_counts = self.get_character_counts(password)
		b_s = 1
		arabic_numerals = len(set(string.digits).intersection(password)) > 0
		lowercase_letters = len(set(string.ascii_lowercase).intersection(password)) > 0
		uppercase_letters = len(set(string.ascii_uppercase).intersection(password)) > 0
		punx = len(self.punx_set.intersection(password)) > 0
		if arabic_numerals:
			b_s += (10 * char_counts[2])
		if lowercase_letters:
			b_s += (26 * char_counts[0])
		if uppercase_letters:
			b_s += (26 * char_counts[1])
		if punx:
			b_s += (33 * char_counts[3])
		return b_s



	def get_transitions(self, password):
		char_flag = []
		t_score = 1 #for scoring purposes, 0 transitions --> t_score of 1
		#char_flag index --> password char index
		#if key for char_flag i --> True, password character is that type
		for i in range(len(password)):
			if password[i] in set(string.ascii_lowercase):
				char_flag.append(1)
			elif password[i] in set(string.ascii_uppercase):
				char_flag.append(2)
			elif password[i] in set(string.digits):
				char_flag.append(3)
			elif password[i] in self.punx_set:
				char_flag.append(4)
		for i in range(len(password)):	
			if char_flag[i] is not char_flag[i + 1 if i + 1 < len(password) else i]: 
				t_score += 1
			else:
				continue
		print "t_score for " + password + ": " + str(t_score)
		return t_score


	def possibly_word(self, password):
		potential_words = 0
		with open(self.wordlist, "r") as wlf:
			for pword in wlf:
				if pword.rstrip("\r\n") in password:
					print "password may contain phrase: " + pword.rstrip("\r\n")
					potential_words += 1
					if pword.rstrip("\r\n") == password:
						potential_words = -1
						print "password found in wordlist!!!"
						break
		wlf.close()
		return potential_words

	def check_for_common_addons(self, password):
		'''
			checks to see if adding strings like:
				* 123
				* 1234
				* 1
				* !
				etc
			result in the password being in the wordlist
			if so, score is reduced by 1/4
		'''
		pass

	def score_password(self, password):
		length = self.get_length(password)
		number_t = self.get_transitions(password)
		base_score = self.get_base_score(password)
		tot = base_score * number_t
		word_count = self.possibly_word(password)
		print "# of possible words: " + str(word_count)
		if word_count <= -1:
			tot = 0
		print "total password score: " +  str(tot)
		print "////////////////////////////////////"
		return tot
		#factor in # of possible words and character counts
		#to do: assign "bad", "good", "very good" ratings based on tot








