import datetime
from utils.fileUtil import fileAppend

def preiodic_check_log(filePath, content):
    time = '[' + str(datetime.datetime.now()) + ']\n'
    fileAppend(filePath, time + content + '\n')