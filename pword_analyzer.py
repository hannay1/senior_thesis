
class Pword_Analyzer:

	def __init__(self):
		self.cpu_factor = 100

	def get_length(self, password):
		return str(len(password))

	def get_character_counts(self, pasword):
		punx = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
		num_punx = [char.match(punx) for char in password].count(True)
		arabic_numerals = [char.isdigit() for char in password].count(True)
		lowercase_letters = [char.islower() for char in password].count(True)
		uppercase_letters = [char.isupper() for char in password].count(True)
		pass

	def get_transitions(self, password):
		pass

	def calculate_strength(self, password):
		pass

