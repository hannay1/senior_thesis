import sys, os, subprocess, tempfile, datetime, time

'''

NEEDS WORK
'''


class MITM_Main:

    def __init__(self):
        self.isUp = False
        self.welcome()

    def switch_ap_on(self):
        '''

            1. take in access point name,
                if name is none, then use STRONGEST ACCESS POINT's name
            2. change access point name in /etc/dhcpd.conf
            3. turn on access point
                EXCEPTIONS:
                    HARDWARE ERRORS
                    ETC
        :return:
        '''
        if not self.isUp:
            print("switching on access point...")
            ap_output = subprocess.Popen(["./RAP.sh" ,"start"],stdout=None, close_fds=True, shell=True, stdin=None, stderr=None)
            #
            print("waiting for RAP.sh to finish...")
            time.sleep(15)
            if "ioctl(SIOCGIFINDEX) failed:" in ap_output.stdout.decode('utf-8'):
                print("Wifi adapter not plugged in")
            else:
                self.isUp = True
                subprocess.Popen("./RAP2.sh", stdout= subprocess.PIPE)
                now = datetime.datetime.now()
                print("access point started at ", now)
        else:
            print("access point is already up")

    def switch_ap_off(self):
        if not self.isUp:
            print("ap isnt even on")
        else:
            subprocess.Popen("./RAP.sh stop", stdout = subprocess.PIPE).communicate()[0]
            self.isUp = False
            print("access point switched off")

    def welcome(self):
        print("*****HEY I'M MALLORY*****")
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
            if resp not in range(1,5):
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
        elif resp == 4:
            sys.exit(0)


def main():
    mal = MalloryMain()

main()
