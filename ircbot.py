# -*- coding: utf-8 -*-
# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, task, defer
from twisted.python import log

# system imports
import time, sys, ConfigParser

# custom imports
from annaop import Manga
from annaop import MangaParser

class MessageLogger:
    def __init__(self, file):
        self.file = file

    def log(self, message):
        timestamp = time.strftime("[%H:%M:%S]", time.localtime(time.time()))
        self.file.write('%s %s\n' % (timestamp, message))
        self.file.flush()

    def close(self):
        self.file.close()

class EnnaOP(irc.IRCClient):
    nickname = "Enna_OP"
    channel = "#OnePieceCircleJerk"

    mangaParser = MangaParser()

    commandList = ["subscribe", "unsubscribe"]

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self._namescallback = {}

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.logger = MessageLogger(open(self.factory.filename, "a"))
        self.logger.log("[connected at %s]" % 
                        time.asctime(time.localtime(time.time())))

        monitorManga = task.LoopingCall(self.BotLoop)
        monitorManga.start(60)

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
        
        # Check to see if they're sending me a private message
        if channel == self.nickname:
            msg = "It isn't nice to whisper!  Play nice with the group."
            self.msg(user, msg)
            return

        # Otherwise check to see if it is a message directed at me
        if msg.startswith(self.nickname + ":"):
            # Check if command is valid before bothering the server
            for cmd in self.commandList:
                if cmd in msg.lower():
                    self.names(self.channel).addCallback(self.commands, user, msg)
                    break

    def commands(self, nicklist, user=None, message=None):
        if not user or not message:
            return

        message = message.lower()
        user = user.lower()
        ircMsg = user + ": "

        userRank = None
        
        # Check if user has OP or voice
        for nick in nicklist:
            if user in nick.lower():
                if nick.startswith("@") or nick.startswith("%"):
                    userRank = "O"
                elif nick.startswith("+"):
                    userRank = "V"

        if not userRank:
            ircMsg += "You need to be voiced to interact with me!"
            self.msg(self.channel, ircMsg.encode("utf8"))
            return

        messageParts = message.split(":")[1].split(" ")

        if "subscribe" in messageParts:
            manga = self.mangaParser.subscribe(message, user)
            if manga:
                ircMsg += "I will notify you for " + manga + " releases."
            else:
                ircMsg += "You are already following this manga or the manga doesn't exist."
            self.msg(self.channel, ircMsg.encode("utf8"))
        elif "unsubscribe" in messageParts:
            manga = self.mangaParser.unsubscribe(message, user)
            if manga:
                ircMsg += "You won't get notified for " + manga + " anymore."
            else:
                ircMsg += "You aren't following this or the manga doesn't exist."
            self.msg (self.channel, ircMsg.encode('utf8'))


    def names(self, channel):
        channel = channel.lower()
        d = defer.Deferred()
        if channel not in self._namescallback:
            self._namescallback[channel] = ([], [])

        self._namescallback[channel][0].append(d)
        self.sendLine("NAMES %s" % channel)
        return d

    def irc_RPL_NAMREPLY(self, prefix, params):
        channel = params[2].lower()
        nicklist = params[3].split(' ')

        if channel not in self._namescallback:
            return

        n = self._namescallback[channel][1]
        n += nicklist

    def irc_RPL_ENDOFNAMES(self, prefix, params):
        channel = params[1].lower()
        if channel not in self._namescallback:
            return

        callbacks, namelist = self._namescallback[channel]

        for cb in callbacks:
            cb.callback(namelist)

        del self._namescallback[channel]

    def BotLoop(self):
        # Check for new releases on MangaStream 
        releases = self.mangaParser.checkForNewReleases(self.mangaParser.parseMangaStream())

        print("I CHECKED MANGAS!!! " + " ".join(releases))

        # Check for new releases on Pota.to

        # Check for new releases on /r/Manga

        for message in releases:
            self.msg("#OnePieceCircleJerk", message.encode('utf8'))

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
