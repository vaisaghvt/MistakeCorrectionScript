
def extractPhrase(match, line):
    """Returns the phrase which was matched """
    startCount=0
    endCount= len(line)
    for i in range(match.start()-1,-1,-1):
        if line[i] == ' ' or line[i] == '\n' or line[i] == '\\':
            startCount =i
            break
    for i in range(match.end(),len(line),1):
        if line[i] == ' ' or line[i] == '\n' or line[i] == '\\':
            endCount =i
            break
    return line[startCount:endCount]

def extractPreviousPhrase(match, line):
    """Returns the phrase which was matched """
    startCount=0
    endCount= 0
    for i in range(match.start()-1,-1,-1):
        if line[i] == ' ' or line[i] == '\n' or line[i] == '\\':
            endCount =i
            break
    for i in range(endCount-1,-1,-1):
        if line[i] == ' ' or line[i] == '\n' or line[i] == '\\':
            startCount =i
            break
    return line[startCount:endCount]

def extractNextPhrase(match, line):
    """Returns the phrase which was matched """
    startCount=0
    endCount= 0
    for i in range(match.end()+1,len(line),1):
        if line[i] == ' ' or line[i] == '\n' or line[i] == '\\':
            startCount =i
            break
    for i in range(startCount+1,len(line),1):
        if line[i] == ' ' or line[i] == '\n' or line[i] == '\\':
            endCount =i
            break
    return line[startCount:endCount]

def paragraphs(fileobj, separator='\n'):
    """Iterate a fileobject by paragraph"""
    ## Makes no assumptions about the encoding used in the file
    lines = []
    for line in fileobj:
        if line == separator and lines:
            yield ''.join(lines)
            lines = []
        else:
            lines.append(line)
    yield ''.join(lines)