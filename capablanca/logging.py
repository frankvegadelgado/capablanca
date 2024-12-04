class SatLogger(object):
    def __init__(self, f):
        self.f = f

    def debug(self, msg, *args, **kwargs):
        self.f.write((msg % args) + '\n')
        
    info = debug

    def warning(self, msg, *args, **kwargs):
        self.f.write('WARNING: ' + (msg % args) + '\n')

    def error(self, msg, *args, **kwargs):
        self.f.write('ERROR: ' + (msg % args) + '\n')

    critical = debug
    
class ConsoleLogger(object):
    def __init__(self, log):
        self.log = log    
    
    def write(self, msg):
        """Logs a message to the console if the global `log` variable is True.

        Args:
            message: The message to be logged.
        """

        if self.log:
            # Using the built-in `print` function is fine for simple logging,
            # but for more advanced logging, consider using the `logging` module.
            print(msg)