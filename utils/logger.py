"""
Logger utility for Termux PXE Boot System
Simple logging utility with configurable levels
"""
import logging
import sys
import os
from datetime import datetime

class Logger:
    def __init__(self, name="TermuxPXE", level=logging.INFO, log_file=None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler if specified
        if log_file:
            try:
                file_handler = logging.FileHandler(log_file)
                file_handler.setLevel(level)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
            except Exception as e:
                self.warning(f"Could not create file handler: {e}")
    
    def debug(self, message):
        """Log debug message"""
        self.logger.debug(message)
    
    def info(self, message):
        """Log info message"""
        self.logger.info(message)
    
    def warning(self, message):
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message):
        """Log error message"""
        self.logger.error(message)
    
    def critical(self, message):
        """Log critical message"""
        self.logger.critical(message)
    
    def set_level(self, level):
        """Set logging level"""
        self.logger.setLevel(level)
        for handler in self.logger.handlers:
            handler.setLevel(level)
