import datetime
from utils.fileUtil import fileAppend

def logToFile(filePath, content):
    time = '\n[' + str(datetime.datetime.now()) + ']\n'
    fileAppend(filePath, time + content)
