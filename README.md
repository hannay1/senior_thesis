# Senior thesis
Implemented a man-in-the-middle platform/rogue WiFi access point. The project is capable of automatically decrypting, identifying, analysing and (securely) recording sensitive information (passwords and session cookies) obtained from TLS-secured traffic through certificate manipulation. This platform was primarily written in Python, using various penetration testing tools compatible with Kali Linux.

The project is also capable of browser hijacking, as well as malware deployment and remote command execution on vulnerable connected machines via client-side attacks. The platform also collects meta-data pertaining to the OS and browser of connected machines. This platform has been successfully tested against Windows, OSX, Linux, iOS, and Android devices.

This project was pitted against various unaware test subjects in a study on end-user security in an ethical and controlled manner.

Requirements:
* Kali Linux
    - mitmproxy
* A USB wireless adapter capable of monitor mode
