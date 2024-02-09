import os

def fileAppend(filePath, content):
    dirPath = os.path.dirname(filePath)
    if not os.path.exists(dirPath):
        os.mkdirs(dirPath)
    with open(filePath, 'a') as f:
        f.write(content)