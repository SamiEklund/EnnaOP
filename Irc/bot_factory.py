""" Module for bot factory """

# twisted imports
from twisted.internet import reactor, protocol

# custom imports
from Irc.enna_op import EnnaOP
from Common.logger import Logger

class BotFactory(protocol.ClientFactory):
    """
    A factory for Bots.
    A new protocol instance will be created each time we connect to the server.
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def buildProtocol(self, addr):
        irc_client = EnnaOP(self.username, self.password)
        irc_client.factory = self
        return irc_client

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        Logger.log("Disconnected from server. Trying to reconnect.")
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        Logger.log("Connection failed, " + reason)
        reactor.stop()
