""" Main program module """

# system imports
import sys
import time
import ConfigParser

# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, task, defer
from twisted.python import log

# custom imports
from Commands.commandcenter import CommandCenter
from Common.data_parser import DataHandler
from Common.manga_parser import MangaParser

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

    commandCenter = CommandCenter()

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self._namescallback = {}

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.logger = MessageLogger(open(self.factory.filename, "a"))
        self.logger.log("[connected at %s]" %
                        time.asctime(time.localtime(time.time())))

        monitor_manga = task.LoopingCall(self.bot_loop)
        monitor_manga.start(60)

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

        if msg.startswith(CommandCenter.COMMAND_PREFIX):
            self.names(self.channel).addCallback(self.commands, user, msg)

    def commands(self, nicklist, user=None, message=None):
        if not user or not message:
            return

        irc_msg = user + ": "

        user_rank = None

        # Check if user has OP or voice
        for nick in nicklist:
            if user.lower() in nick.lower():
                if nick.startswith("@") or nick.startswith("%"):
                    user_rank = "O"
                elif nick.startswith("+"):
                    user_rank = "V"

        if not user_rank:
            irc_msg += "You need to be voiced to interact with me!"
            self.msg(self.channel, irc_msg.encode("utf8"))
            return

        irc_msg += self.commandCenter.parse_and_execute(user, message)
        self.msg(self.channel, irc_msg.encode("utf8"))

    def names(self, channel):
        """ Gets list of nicks on the channel """
        channel = channel.lower()
        promise = defer.Deferred()
        if channel not in self._namescallback:
            self._namescallback[channel] = ([], [])

        self._namescallback[channel][0].append(promise)
        self.sendLine("NAMES %s" % channel)
        return promise

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

    def bot_loop(self):
        """ Monitors data sources and reports new finds to irc channel """

        new_releases = []

        for source in DataHandler.data_sources:
            print "Checking soruse " + source.source_url
            if source.data_type == "rss":
                print "Checking RSS site: " + source.source_url
                release_list = DataHandler.get_manga_from_rss(source)
                print "Got the releases! Checking if any new releases!"
                new_releases += MangaParser.check_for_new_releases(release_list)
                print "Checked the releases! So far " + str(len(new_releases)) + " new releases!"

        for release in new_releases:
            self.msg("#OnePieceCircleJerk", release.get_release_message().encode('utf8'))

class BotFactory(protocol.ClientFactory):
    """
    A factory for Bots.
    A new protocol instance will be created each time we connect to the server.
    """

    def __init__(self, username, password):
        self.filename = "logfile.log"
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
