""" Main program module """

# system imports
import ConfigParser

# twisted imports
from twisted.internet import reactor

# custom imports
from Irc.bot_factory import BotFactory

if __name__ == '__main__':
    # Read config file
    CONFIG = ConfigParser.RawConfigParser()
    CONFIG.read('conf.config')

    SERVER_IP = CONFIG.get('server', 'ip')
    SERVER_PORT = CONFIG.getint('server', 'port')
    SERVER_USERNAME = CONFIG.get('server', 'username')
    SERVER_PASSWORD = CONFIG.get('server', 'password')

    # Start bot
    FACOTRY = BotFactory(SERVER_USERNAME, SERVER_PASSWORD)
    reactor.connectTCP(SERVER_IP, SERVER_PORT, FACOTRY)
    reactor.run()
