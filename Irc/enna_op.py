""" Module for twisted irc client """

# twisted imports
from twisted.words.protocols import irc
from twisted.internet import task, defer

# custom imports
from Commands.commandcenter import CommandCenter
from Common.data_parser import DataHandler
from Common.manga_parser import MangaParser
from Common.logger import Logger

class EnnaOP(irc.IRCClient):
    """ Main bot logic and communicates with IRC """
    nickname = "Enna_OP"
    channel = "#OnePieceCircleJerk"

    commandCenter = CommandCenter()

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self._namescallback = {}

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        Logger.log("Connected to IRC? Server? Channel?")

        # Start bot tasks
        monitor_manga = task.LoopingCall(self.bot_loop)
        monitor_manga.start(60)

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        Logger.log("[Disconnected!")

    # callbacks for events

    def signedOn(self):
        Logger.log("Signed on to server!")

    def privmsg(self, user, channel, msg):
        user = user.split('!', 1)[0]

        # Check to see if they're sending me a private message
        if channel == self.nickname:
            msg = "Hello! I am illegal bot and I don't have registered nick nor vhost/cloak!"
            self.msg(user, msg)
            return

        # Otherwise check to see if it is a message directed at me

        if msg.startswith(CommandCenter.COMMAND_PREFIX):
            self.names(self.channel).addCallback(self.validate_and_execute_command, user, msg)

    def validate_and_execute_command(self, nicklist, user=None, message=None):
        """ Checks user permissions and executes command and answers to IRC """
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
            Logger.log("User without voice tried to interract with me! User %s | Message: %s" %
                       (user, message))
            irc_msg += "LALALALA! I CAN'T HEAR YOU! (you need to be voiced)"
            self.msg(self.channel, irc_msg.encode("utf8"))
            return

        command_feedback = self.commandCenter.parse_and_execute(user, message)
        if command_feedback is not "":
            irc_msg += command_feedback
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
        """
            This method is from twisted.words.im.ircsupport.IRCProto
            I don't know how this works
        """
        channel = params[2].lower()
        nicklist = params[3].split(' ')

        if channel not in self._namescallback:
            return

        nicks = self._namescallback[channel][1]
        nicks += nicklist

    def irc_RPL_ENDOFNAMES(self, prefix, params):
        """
            This method is from twisted.words.im.ircsupport.IRCProto
            I don't know how this works
        """
        channel = params[1].lower()
        if channel not in self._namescallback:
            return

        callbacks, namelist = self._namescallback[channel]

        for callback in callbacks:
            callback.callback(namelist)

        del self._namescallback[channel]

    def bot_loop(self):
        """ Monitors data sources and reports new finds to irc channel """

        new_releases = []

        for source in DataHandler.data_sources:
            Logger.log("Checking soruse " + source.source_url)
            if source.data_type == "rss":
                Logger.log("Checking RSS site: " + source.source_url)
                release_list = DataHandler.get_manga_from_rss(source)
                Logger.log("Got the releases! Checking if any new releases!")
                new_releases += MangaParser.check_for_new_releases(release_list)
                Logger.log("Checked the releases! So far " + str(len(new_releases)) %
                           " new releases!")

        for release in new_releases:
            self.msg("#OnePieceCircleJerk", release.get_release_message().encode('utf8'))
