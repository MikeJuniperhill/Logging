import datetime as dt   
import enum

class LogLevel(enum.Enum):
    debug = 1
    info = 2
    warning = 3
    error = 4
    critical = 5
    
# subscriber in observer pattern, receives updates from publisher.
class LogHandler:
    def __init__(self, logging_function, log_level):
        self.logging_function = logging_function
        self.log_level = log_level
    
    # receive update from publisher
    def update_log(self, message, log_level):
        # log levels: debug=1, info=2, warning=3, error=4, critical=5
        # ex. class log level 1 will send log updates for all incoming messages
        if(self.log_level.value <= log_level.value):
            date_time_string = str(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            self.logging_function('{} {} {}'.format(date_time_string, log_level.name, message))
        
# publisher in observer pattern, send updates for subscribers.
class Logger:
    def __init__(self):
        self.log_handlers = set()
        
    def register_log_handler(self, log_handler):
        self.log_handlers.add(log_handler)
        
    def unregister_log_handler(self, log_handler):
        self.log_handlers.discard(log_handler)
    
    # send update for all registered subscribers
    def send_log_update(self, message, log_level):
        for log_handler in self.log_handlers:
            log_handler.update_log(message, log_level)  

# create publisher
logger = Logger()

# create console log handler, receiving updates only when update message log level is greater than/equal to warning
console_log_handler = LogHandler(lambda message: print(message), LogLevel.warning)
logger.register_log_handler(console_log_handler)

# create file log handler, receiving all possible updates
log_file = open('/home/mikejuniperhill/log.txt', 'w')
file_log_handler = LogHandler(lambda message: print(message, file=log_file), LogLevel.debug)
logger.register_log_handler(file_log_handler)

# process log updates
logger.send_log_update('sending calculation task to engine', LogLevel.debug)
logger.send_log_update('engine is processing calculation task', LogLevel.info)
logger.send_log_update('incorrect grid configurations, using backup grid settings', LogLevel.warning)
logger.send_log_update('analytical error retrieved for this calculation task', LogLevel.error)
logger.send_log_update('unable to process calculations task due to incorrect market data', LogLevel.critical)

log_file.close()

# console output:
# 2020-03-14 12:56:09 warning incorrect grid configurations, using backup grid settings
# 2020-03-14 12:56:09 error analytical error retrieved for this calculation task
# 2020-03-14 12:56:09 critical unable to process calculations task due to incorrect market data

