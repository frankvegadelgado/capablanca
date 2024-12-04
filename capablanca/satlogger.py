class SatLogger:
    def __init__(self, logger):
        self.logger = logger
   
    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

class ConsoleLogger(object):
    
    def __init__(self, log):
        self.log = log    
    
    def info(self, msg, *args, **kwargs):
        """Logs a message to the console if the `log` variable is True.

        Args:
            message: The message to be logged.
        """

        if self.log:
            # Using the built-in `print` function is fine for simple logging,
            # but for more advanced logging, consider using the `logging` module.
            print(msg)