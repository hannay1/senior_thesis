import string, math
from decimal import Decimal

class Pword_Analyzer:

	def __init__(self):
		self.cpu_factor = 1000000 #num guesses/sec
		self.wordlist = "passwords_john.txt"
		self.punx_set = set(string.punctuation)
		self.punx_set.update(' ')

	def get_character_counts(self, password):
		num_punx = [char in self.punx_set for char in password].count(True)
		arabic_numerals = [char in set(string.digits) for char in password].count(True)
		lowercase_letters = [char in set(string.ascii_lowercase) for char in password].count(True)
		uppercase_letters = [char in set(string.ascii_uppercase) for char in password].count(True)
		tup = (lowercase_letters, uppercase_letters, arabic_numerals, num_punx)
		print "*** lowercase_letters: " + str(lowercase_letters)
		print "*** uppercase_letters:" + str(uppercase_letters)
		print "*** arabic_numerals:" + str(arabic_numerals)
		print "*** punctuation:" + str(num_punx)
		return tup

	def get_base_score(self, password):
		print "**** GENERAL INFO *****"
		char_counts = self.get_character_counts(password)
		b_s = 1
		e_t = 0
		if char_counts[2] > 0:
			b_s += (10 * char_counts[2])
			e_t += 10
		if char_counts[0] > 0:
			b_s += (26 * char_counts[0])
			e_t += 26
		if char_counts[1] >0:
			b_s += (26 * char_counts[1])
			e_t += 26
		if char_counts[3] > 0:
			b_s += (33 * char_counts[3])
			e_t += 33
		if e_t == 0:
			return 0, 0
		return b_s, self.entropy(e_t, password)



	def get_transitions(self, password):
		print "***** TRANSITIONS ****"
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
		print "t_score for " + password + ": " + str(t_score -1) + " transitions"
		return t_score 


	def possibly_word(self, password):
		print "***** BRUTE FORCING *****"
		potential_words = 0
		with open(self.wordlist, "r") as wlf:
			for pword in wlf:
				if pword.rstrip("\r\n") in password:
					print "[ALMOST] password contains string: " + pword.rstrip("\r\n")
					potential_words += len(pword.rstrip("\r\n"))
					if pword.rstrip("\r\n") == password:
						potential_words = -1
						print "[HIT!] password found in wordlist!!!"
						break
		wlf.close()
		return potential_words

	def score_password(self, password):
		number_t = self.get_transitions(password)
		base_score, entropy = self.get_base_score(password)
		word_count = self.possibly_word(password)
		print "# of possible words: " + str(word_count)
		edit_count, closest_password = self.edit_distance(password)
		try:
			tot = math.log((float(base_score * (number_t+1) * entropy +1)/float(word_count)) * edit_count) if edit_count is not 0 else 0
		except ZeroDivisionError as ze:
			print "hi"
			tot = math.log((float(base_score * (number_t+1) * entropy +1) * edit_count)) if edit_count is not 0 else 0
		print ("****** FINAL SCORE ******")
		print "total password score: " +  str(tot)
		print "////////////////////////////////////"
		return (tot, edit_count, number_t)


	def entropy(self, et, password):
		return float(et**len(password) / self.cpu_factor)


	def edit_distance(self,password1):
		print "****** EDIT DISTANCE *******"
		try:
			with open(self.wordlist, "r") as wlf:
				dists = {}
				for pword in wlf:
					password2 = pword.rstrip("\r\n")
					str_len = len(password1) if len(password1) > len(password2) else len(password2)
					tabe = [[0 for i in range(str_len +1)] for j in range(str_len +1)]
					for x in range(0, len(tabe[0])):tabe[0][x] = x
					for y in range(0, len(tabe[0])):tabe[y][0] = y
					for a in range(1, len(password1) +1):
						for b in range(1, len(password2) +1):
							if password1[a-1] == password2[b-1]:
								#same --> diagonal
								tabe[a][b] = tabe[a-1][b-1]
							else:
								#different --> 1 + min of (a,b,c)
								tabe[a][b] = min(tabe[a-1][b-1] + 1, tabe[a-1][b] +1, tabe[a][b-1] +1)
					dists[password2] = (tabe[len(password1)][len(password2)])
				#ratio = 1.0 - (float(tabe[len(string1)][len(string2)]) / float((max(len(string1), len(string2)))))
				min_dist = min(dists, key=dists.get)
				print"closest [password] : " +  str(min_dist) + " | edit distance: " + str(dists[min_dist])
				#print"percent same as " + str(dists[min_dist]) +  " :" + str(ratio)
				return dists[min_dist], str(min_dist)
		except Error as fnfe:
			print fnfe
			


#sign beef with mitm private key 

if __name__ == "__main__":
	pwa = Pword_Analyzer()
	pwa.score_password(str("RightHa!ndMan34?*"))
