import logging
from imp import reload

def logToFile(path, logsString):
    reload(logging)
    logging.basicConfig(filename=path, level=logging.DEBUG, filemode="w", format="%(message)s")
    logging.info(logsString)
