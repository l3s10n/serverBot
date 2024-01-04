def fileAppend(filePath, content):
    with open(filePath, 'a') as f:
        f.write(content)