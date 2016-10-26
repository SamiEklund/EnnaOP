# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, threads
from twisted.python import log

# system imports
import time, sys, ConfigParser

# custom imports


class MessageLogger:
    def __init__(self, file):
        self.file = file

    def log(self, message):
        timestamp = time.strftime("[%H:%M:%S]", time.localtime(time.time()))
        self.file.write('%s %s\n' % (timestamp, message))
        self.file.flush()

    def close(self):
        self.file.close()

def TestMethod(bot):
    import time
    while True:
        bot.threadSafeMsg("CHANNEL", "Just testing this loopy loop")
        time.sleep(5)

class EnnaOP(irc.IRCClient):
    nickname = "Enna_OP"

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.logger = MessageLogger(open(self.factory.filename, "a"))
        self.logger.log("[connected at %s]" % 
                        time.asctime(time.localtime(time.time())))
        # TODO Start luup
        threads.deferToThread(TestMethod, self)

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        self.logger.log("[disconnected at %s]" % 
                        time.asctime(time.localtime(time.time())))
        self.logger.close()

    # callbacks for events

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        # self.join(self.factory.channel)

    def joined(self, channel):
        """This will get called when the bot joins the channel."""
        self.logger.log("[I have joined %s]" % channel)

    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""
        user = user.split('!', 1)[0]
        self.logger.log("<%s> %s" % (user, msg))
        
        # Check to see if they're sending me a private message
        if channel == self.nickname:
            msg = "It isn't nice to whisper!  Play nice with the group."
            self.msg(user, msg)
            return

        # Otherwise check to see if it is a message directed at me
        if msg.startswith(self.nickname + ":"):
            msg = "%s: I am the bot who will become the next Anna_OP!" % user
            self.msg(channel, msg)
            self.logger.log("<%s> %s" % (self.nickname, msg))

    def threadSafeMsg(self, channel, message):
        reactor.callFromThread(self.msg, channel, message)

class BotFactory(protocol.ClientFactory):
    """
    A factory for Bots.
    A new protocol instance will be created each time we connect to the server.
    """

    def __init__(self, username, password):
        self.filename = "logfile.txt"
        self.username = username
        self.password = password

    def buildProtocol(self, addr):
        p = EnnaOP(self.username, self.password)
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()


if __name__ == '__main__':
    # Read config file
    config = ConfigParser.RawConfigParser()
    config.read('conf.config')

    server_ip = config.get('server', 'ip')
    server_port = config.getint('server', 'port')
    server_username = config.get('server', 'username')
    server_password = config.get('server', 'password')

    log.startLogging(sys.stdout)
    
    f = BotFactory(server_username, server_password)
    reactor.connectTCP(server_ip, server_port, f)
    reactor.run()
