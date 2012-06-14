from extractPhrases import *        

def checkPattern(option, match, line):
    if option =='t':
        return isInTag(extractPhrase(match, line))
    elif option =='a':
         return isAcronym(extractPhrase(match, line))
    elif option =='c':
        return isComment(match, line)
    elif option =='e':
       return isEquation(match, line)
    elif option =='i':
       return isInComplete(match, line)

def isAcronym(phrase):
    '''Returns a true if the match is an acronym'''
#    print "testing if", phrase, "is an acronym"
    if(phrase.rfind('i.e.')!=-1 
        or phrase.rfind('e.g.')!=-1 
        or phrase.rfind('etc.')!=-1):
#        print "returning true"
        return True
    else :
        return False

def isInTag(phrase):
    '''Returns a true if the match is any tag'''
    if(phrase.rfind('\\')==0):
        return True
    else :
        return False

def isInCite(phrase):
    '''Returns a true if the match is in Cite'''
    if(phrase.rfind(r'\cite')==0):
        return True
    else :
        return False

def inLineEquation(match, line):
    """ Returns true if in inline equation"""
    hasDollarTagBefore=False
    for i in range(match.start()-1,-1,-1):
        if line[i] == '$':
            hasDollarTagBefore=True
            break
    if hasDollarTagBefore:
        for i in range(match.end(),len(line),1):
            if line[i] == '$':
                return True
    return False
    
def inEquationBody(match, line):
    # print 'checking equation', match.start()-1
    end= line[0:match.start()].rfind(r'\end{equation}')
    pos= 0
    while(end!=-1):
        pos= end
        end= line[pos:match.start()].rfind(r'\end{equation}')
    beg=line[pos:match.start()].rfind(r'\begin{equation}')
    if(beg!=-1):
        return True     
    return False

def isEquation(match, line):
    if(inLineEquation(match,line) or inEquationBody(match, line)):
       return True
    else:
       return False

def isComment(match, line):
    for i in range(match.start()-1,-1,-1):
        # print line[i]
        if line[i] == '\n':
            break
        if line[i] == '%':
            return True
    return False

def isInComplete(match, para):
    # print para[match.start():match.end()]
    if not (para[match.start()] == ' ' or para[match.start()] == '\n'):
        # print "not starting with space"
        if match.start()-1>=0:
            firstLetter = para[match.start()-1]
            # print "first:", firstLetter
            if not (firstLetter == ' ' or firstLetter == '\n'):
                return True
    if not (para[match.end()-1] == ' ' or para[match.end()-1] == '\n'):
        # print "not ending with space"
        if match.end()<len(para):
            lastLetter = para[match.end()]
            # print "last",lastLetter
            if not (lastLetter == ' ' or lastLetter == '\n'):
                return True
    return False