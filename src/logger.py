"""
Logger
SPDX-License-Identifier: LGPL-3.0-or-later
Auteurs: Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
import logging
import sys

class Logger:
    """
    This class logs messages to the terminal. 
    
    If you would like to view the logs as they are written to a file rather than in the terminal, set the argument log_to_file to True and run `tail -f src/store_manager.log` in your Linux terminal.
    """
    
    @staticmethod
    def get_instance(name: str, level=logging.DEBUG, log_to_file=False):
        """ Set up a logger to stdout. Works for both the Docker terminal and the host machine terminal """
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.propagate = False
        
        if logger.handlers:
            return logger
        
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console Handler (stdout)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler (.log file)
        if (log_to_file):
            fileHandler = logging.FileHandler("store_manager.log")
            fileHandler.setFormatter(formatter)
            logger.addHandler(fileHandler)
        
        # Ensure root logger doesn't interfere
        logging.root.setLevel(logging.WARNING)
        
        return logger