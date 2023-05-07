import irc

def on_start():
    print()
    client.joinchan("#general")
def on_message(message, name):
    if message.rstrip() == "!test":
        client.sendmsg("Hello!", "#general")

server = "FILLER"
port = 6697
nickname = "FILLER"
exitword = "FILLER"
adminname = "FILLER"


client = irc.Client(server, port, nickname, exitword, adminname, on_start, on_message)



client.connect()