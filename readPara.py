import itertools as it
import re
import os
import Getch as gc

fileName = "random.txt"


def removeSpaceBeforePunctuation(match, para):
    for i in range(match.start(), match.end(), 1):
        if para[i] == " ":
            newPara = para[0:i] + para[i+1:len(para)]
    return newPara

def addSpaceAfterPunctuation(match, para):
    for i in range(match.start(), match.end(), 1):
        if para[i] == "." or para[i] == "," or para[i] == ";" or para[i] == ":":
            newPara = para[0:i+1] + " " +para[i+1:len(para)]
    return newPara

def capitalizeFirst(match, para):
    for i in range(match.start(), match.end(), 1):
        if para[i] == " ":
            newPara = para[0:i+1] + para[i+1].upper() +para[i+2:len(para)]
    return newPara

def addTildeBeforeCite(match, para):
    for i in range(match.start(), match.end(), 1):
        if para[i] == "\\":
            if para[i-1]==' ':
                newPara = para[0:i-1]+"~" +para[i:len(para)]
            else:
                newPara = para[0:i]+"~" +para[i:len(para)]
    return newPara

def capitalizeChapter(match, para):
    for i in range(match.start(), match.end(), 1):
        if para[i] == "c":
            newPara = para[0:i] + para[i].upper() +para[i+1:len(para)]
    return newPara

def capitalizeSection(match, para):
    for i in range(match.start(), match.end(), 1):
        if para[i] == "s":
            newPara = para[0:i] + para[i].upper() +para[i+1:len(para)]
    return newPara

# Store this in a dictionary with a short hand description, tags and the replacementFunction for the tag
patterns = {r' [\.,;:]':["SPACE BEFORE PUNCTUATION.",'tace',removeSpaceBeforePunctuation],
            r'[\.,;:][a-zA-Z]':["NO SPACE AFTER PUNCTUATION.",'tace',addSpaceAfterPunctuation] ,
            r'([\.] [a-z])|^[a-z]':["MISSING CAPITALIZATION OF FIRST WORD AFTER FULL STOP.",'tace',capitalizeFirst],
            r'[^~]\\cite|[^~]\\ref':["TILDE MARK NEEDED BEFORE CITE",'ace',addTildeBeforeCite],
            r'([^C]|c)hapter~\\ref':["CAPITALIZE C IN CHAPTER", 'ce', capitalizeChapter],
            r'([^S]|s)ection~\\ref':["CAPITALIZE S IN SECTION", 'ce', capitalizeSection]}




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
    '''Returns a true if the match is any tag'''
    if(phrase.rfind(r'\cite')==0):
        return True
    else :
        return False

def inLineEquation(match, line):
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

def checkPattern(option, match, line):
    if option =='t':
        return isInTag(extractPhrase(match, line))
    elif option =='a':
         return isAcronym(extractPhrase(match, line))
    elif option =='c':
        return isComment(match, line)
    elif option =='e':
       return isEquation(match, line)



def dealWithIt(match, para, replacementFunction):
    replacement =  suggestReplacement(match, para, replacementFunction)
    while True:
        print "Suggested replacement:",replacement
        print "(a)ccept suggestion | (i)gnore:",
        option = gc.getch()
        print option
        if option == 'a':
            return replacement
        # elif option == 'e':
        #     print "code to edit and write own correction here"
        #     return getReplacement(match, para)
        elif option == 'i':
            print "ignored... "
            return para
            break
        else :
            print "invalid choice"

def suggestReplacement(match, para, replacementFunction):
    return replacementFunction(match, para)

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

def writeToFile(group):
    # for para in group:
    #     print para  
    tempFileName = fileName +".temp"  
    with open(tempFileName,"w") as writeFile:
        for para in group:
            writeFile.write(para+'\n')
    os.remove(fileName)
    os.rename(tempFileName,fileName)

# write as seperate module
#Also, try to seperate itemize , etc. maybe have another function to slice it further.


# paragraph_lists = []

group = []
with open(fileName) as f:
    paras = paragraphs(f)
    for para in paras:
        group.append(para)
count=0
# print group
newContent =""
matched = False
for pattern in patterns.keys():
    # print count 
    count=count+1
    flag = False
    for index, para in enumerate(group):
        regex = re.compile(pattern)
        # m = re.findall(pattern,line)
    #   writeFile.write(line.replace("tutu","random"))

        for match in regex.finditer(para):
            for option in patterns[pattern][1]:
                if(checkPattern(option, match, para)):
                    flag= True
                    break
            if flag:
                flag = False
                continue
            matched = True
            print "Problem: ", patterns[pattern][0],"; Para", count
            print "Phrase: ", extractPhrase(match,para)
            # print "context: ",para
            group[index] = dealWithIt(match, para, patterns[pattern][2])
            para= group[index]            
            print "**********************"
if matched != True:
    print "No mistakes found. Good Stuff!"
writeToFile(group)




    