import irc

def on_start():
    for channel in client.listchans():
        client.joinchan(channel)
def on_message(message, name):
    if message.rstrip() == "!test":
        client.sendmsg("Hello!", "#general")
def on_ping():
    for channel in client.listchans():
        client.joinchan(channel)




server = "FILLER"
port = 6697
nickname = "FILLER"
exitword = "FILLER"
adminname = "FILLER"


client = irc.Client(server, port, nickname, exitword, adminname, on_start=on_start, on_message=on_message, on_ping=on_ping)



client.connect()