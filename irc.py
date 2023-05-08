import socket
import sys

def getip(URL):
    try:
        return socket.gethostbyname(URL)
    except socket.error:
        return URL

def stub():
    pass

class Client:
    def __init__(self, server, port, botnick, exitcode, adminname, on_start=stub, on_message=stub, on_ping=stub):
        self.server = server
        self.port = port
        self.botnick = botnick
        self.exitcode = exitcode
        self.adminname = adminname
        self.on_start = on_start
        self.on_message = on_message
        self.on_ping = on_ping
        self.channels = []

        # used by self.connect()
        self.ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    # connects and runs the bot
    def connect(self):
        remote_ip = getip(self.server)
        try:
            self.ircsock.connect((remote_ip, self.port))
        except ConnectionRefusedError:
            print("The server refused your connection and the program will exit now.")
            sys.exit()
        self.ircsock.send(bytes("USER "+ self.botnick +" "+ "0" +" "+ self.botnick + " :" + self.botnick + "\n", "UTF-8"))
        self.ircsock.send(bytes("NICK "+ self.botnick +"\n", "UTF-8"))
        #self.ircsock.send(bytes("PRIVMSG nickserv :iNOOPEn", "UTF-8"))
        self.main()

    def listchans(self):
        self.ircsock.send(bytes("LIST \n", "UTF-8"))
        channels = []
        ircmsg = ""
        ircmsg = self.ircsock.recv(2048).decode("UTF-8").split("\n")
        for line in ircmsg:
            print(line)
            if line.find("322 " + self.botnick) != -1:
                channels += [line.split("322 ")[1].split(" ")[1]]
        return channels
                

    def joinchan(self, chan): 

        if chan in self.channels:
            return
        self.ircsock.send(bytes("JOIN "+ chan +"\n", "UTF-8"))
        ircmsg = ""
        self.channels += [chan]
        while ircmsg.find("End of /NAMES list.") == -1:
            ircmsg = self.ircsock.recv(2048).decode("UTF-8")
            ircmsg = ircmsg.strip('nr')
            print(ircmsg)

    #responds to server pings
    def pong(self):
        self.ircsock.send(bytes("PONG :pingis\n", "UTF-8"))

    def sendmsg(self, msg, target):
        self.ircsock.send(bytes("PRIVMSG "+ target +" :"+ msg +"\n", "UTF-8"))

    def main(self):
        while True:
            ircmsg = self.ircsock.recv(2048).decode("UTF-8")
            ircmsg = ircmsg.strip('nr')
            print(ircmsg)

            if ircmsg.find("376 " + self.botnick) != -1:
                self.on_start()
            elif ircmsg.find("PING :") != -1:
                self.pong()
                self.on_ping()
            elif ircmsg.find("PRIVMSG") != -1:
                name = ircmsg.split('!',1)[0][1:]
                message = ircmsg.split('PRIVMSG',1)[1].split(':',1)[1]
                if len(name) < 17:
                    if name.lower() == self.adminname.lower() and message.rstrip() == self.exitcode:
                        self.ircsock.send(bytes("QUIT \n", "UTF-8"))
                        return
                    else:
                        self.on_message(message, name)