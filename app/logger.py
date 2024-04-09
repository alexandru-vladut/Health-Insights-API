'''
This module contains the logger class that is used to log messages to a file.
'''

import logging

from datetime import datetime, timedelta, timezone
from logging.handlers import RotatingFileHandler

class MyLogger:
    '''
    This class is used to log messages to a file.
    '''

    def __init__(self):
        self.logger = logging.getLogger('MyAppLogger')
        self.logger.setLevel(logging.INFO)

        # Create a RotatingFileHandler
        handler = RotatingFileHandler('webserver.log', maxBytes=500*150, backupCount=5)

        # Define a formatter with a custom time format in UTC
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
        formatter.datefmt = "%d-%m-%Y %H:%M:%S"
        formatter.formatTime = self.utc_formatter

        # Set formatter for the handler
        handler.setFormatter(formatter)

        # Add the handler to the logger
        self.logger.addHandler(handler)

        self.logger.info("Server started")

    @staticmethod
    def utc_formatter(record, datefmt):
        '''
        This function is used to convert the UTC time to Bucharest time.
        '''

        # Create a datetime object from the timestamp in UTC
        utc_dt = datetime.fromtimestamp(record.created, timezone.utc)

        # Convert the UTC time to Bucharest time
        bucharest_dt = utc_dt + timedelta(hours=3)

        return bucharest_dt.strftime(datefmt)

    def info(self, message):
        '''
        This function is used to log an info message.
        '''

        self.logger.info(message)

    def error(self, message):
        '''
        This function is used to log an error message.
        '''

        self.logger.error(message)
