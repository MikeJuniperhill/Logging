import os, logging, json

class Configurations:
    inner = {}
    # read JSON configuration file to dictionary
    def __init__(self, filePathName):
        self.inner = json.load(open(filePathName))
    # return value for a given configuration key
    # 'overload' indexing operator
    def __getitem__(self, key):
        return self.inner[key.upper()]

def Initialize_logHandlers(configurations):
    """
    Description: create log handlers for console and file stream, based on given configurations.
    Pre-condition: configurations object must have been created before entering into this method.
    Post-condition: logging for console and file stream is available.
    Returns: none.
    Exception handling: none.
    """
    # conditionally, delete the existing log file before starting to write log for this session
    if(bool(int(configurations['CleanLogFileBeforeWrite'])) == True):
        path = configurations['LogFilePath']
        if(os.path.exists(path) == True): os.remove(path)
 
    # create logger
    logger = logging.getLogger()
    logger.setLevel(logging.NOTSET)
 
    # console log handler
    c_handler = logging.StreamHandler()
    c_handler.setLevel(int(configurations['ConsoleLogLevel']))
    c_formatter = logging.Formatter(configurations['LogFormatString'], datefmt=configurations['LogDateFormat'])
    c_handler.setFormatter(c_formatter)
    logger.addHandler(c_handler)
 
    # file log handler
    f_handler = logging.FileHandler(configurations['LogFilePath'], mode=configurations['LogFileMode'], encoding=None, delay=True)
    f_handler.setLevel(int(configurations['FileLogLevel']))
    f_formatter = logging.Formatter(configurations['LogFormatString'], datefmt=configurations['LogDateFormat'])
    f_handler.setFormatter(f_formatter)
    logger.addHandler(f_handler)

# read configurations for this program
path = '/home/mikejuniperhill/configurations.json'
# create configurations object
configurations = Configurations(path)

# initialize log handlers
Initialize_logHandlers(configurations)
 
# process log updates
logging.debug('sending calculation task to engine')
logging.info('engine is processing calculation task')
logging.warning('incorrect grid configurations, using backup grid settings')
logging.error('analytical error retrieved for this calculation task')
logging.critical('unable to process calculations task due to incorrect market data')
