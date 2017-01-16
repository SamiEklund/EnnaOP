""" Module for the static logger that logs """

import time
import datetime

def init_logger():
    """ Creates new log file """
    timestamp = datetime.datetime.utcnow().strftime("%Y-%M-%d-%H-%M-%S")
    log_file = open("logs/log_enna_op-" + timestamp, "a")
    log_file.write("New logfile started at %s" % (timestamp))
    return log_file

class Logger(object):
    """ Static class that logs """

    log_file = init_logger()

    @staticmethod
    def log(message):
        """ Logs message to log file and to console """
        print message
        timestamp = time.strftime("[%H:%M:%S]", time.localtime(time.time()))
        Logger.log_file.write('%s %s\n' % (timestamp, message))
        Logger.log_file.flush()

    @staticmethod
    def close():
        """ Closes the log file """
        Logger.log_file.close()
