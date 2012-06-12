def removeSpaceBeforePunctuation(match, para):
    if match.start()==0:
        newPara = para[1:len(para)]
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
    if match.start()==0:
        newPara = para[0].upper() +para[1:len(para)]
    for i in range(match.start(), match.end(), 1):
        if para[i] == " ":
            newPara = para[0:i+1] + para[i+1].upper() +para[i+2:len(para)]
    return newPara

def removeExtraSpaces(match, para):   
    return para[0: match.start()]+" "+para[match.end():len(para)]

def addTildeBeforeCite(match, para):
    for i in range(match.start(), match.end(), 1):
        if para[i] == "\\":
            if para[i-1]==' ':
                newPara = para[0:i-1]+"~" +para[i:len(para)]
            else:
                newPara = para[0:i]+"~" +para[i:len(para)]
    return newPara



def capitalizeChapter(match, para):
    if match.start()==0:
        newPara = para[0].upper() +para[1:len(para)]
    for i in range(match.start(), match.end(), 1):
        if para[i] == "c":
            newPara = para[0:i] + para[i].upper() +para[i+1:len(para)]
    return newPara

def capitalizeSection(match, para):
    if match.start()==0:
        newPara = para[0].upper() +para[1:len(para)]
    for i in range(match.start(), match.end(), 1):
        if para[i] == "s":
            newPara = para[0:i] + para[i].upper() +para[i+1:len(para)]
    return newPara

def extractNextWord(pos, para):
    word = ""
    for i in range(pos, len(para), 1):
        if(para[i]==' ' or not isAlpha(para[i])):
            return word, i
        else:
            word += para[i]

def capitalizeFirstLetter(word):
    return toUpper(word[0]) + word[1: len(word)]

def uncapitalizeFirstLetter(word):
    return toLower(word[0]) + word[1: len(word)]

def notFullyCapital(word):
    for i in range(0,len(word),1):
        if(isLower(word[i])):
            return True
    return False

def convertToTitleCase(match, para):
    for i in range(match.end(), len(para), 1):
        if para[i] == '{':
            pos =i
            break
    newPara = para[0:pos]
    count =1
    forceCapitalize = True
    while pos < len(para):
        if(para[pos]=='{'):
            count+=1
            newPara += para[pos]
        elif(para[pos]=='}'):
            count-=1
            newPara += para[pos]
            if(count==0):
                break
        if(isAlpha(para[pos])):
            nextWord, pos = extractNextWord(pos, para)
            if(forceCapitalize):
                newPara+= capitalizeFirstLetter(nextWord)
                forceCapitalize = False
            elif(nextWord not in('and', 'the', 'or','on', 'at', 'in')):
                newPara+= capitalizeFirstLetter(nextWord)
        else:
            newPara+= para[pos]
        pos+=1
    newPara += para[pos: len(para)]


def convertFirstLetterToCapital(match, para):
    for i in range(match.end(), len(para), 1):
        if para[i] == '{':
            pos =i
            break
    newPara = para[0:pos]
    count =1
    forceCapitalize = True
    while pos < len(para):
        if(para[pos]=='{'):
            count+=1
            newPara += para[pos]
        elif(para[pos]=='}'):
            count-=1
            newPara += para[pos]
            if(count==0):
                break
        if(isAlpha(para[pos])):
            nextWord, pos = extractNextWord(pos, para)
            if(forceCapitalize):
                newPara+= capitalizeFirstLetter(nextWord)
                forceCapitalize = False
            elif(notFullyCapital(nextWord)):
                newPara+= uncapitalizeFirstLetter(nextWord)
        else:
            newPara+= para[pos]
        pos+=1
    newPara += para[pos: len(para)]

   


def removeRepeatedPhrase(match ,para):
    newpara= para[0:match.start()]+ para[match.start():match.start()+ (match.end()-match.start())/2]+para[match.end()-1:len(para)]
    return newpara


# Store this in a dictionary with a short hand description, tags and the replacementFunction for the tag
patterns = {r' [\.,;:]':["SPACE BEFORE PUNCTUATION.",'tace',removeSpaceBeforePunctuation],
            r'[\.,;:][a-zA-Z]':["NO SPACE AFTER PUNCTUATION.",'tace',addSpaceAfterPunctuation] ,
            r'([\.] [a-z])|^[a-z]':["MISSING CAPITALIZATION OF FIRST WORD AFTER FULL STOP.",'tace',capitalizeFirst],
            r'[^~]\\cite|[^~]\\ref':["TILDE MARK NEEDED BEFORE CITE",'ace',addTildeBeforeCite],
            r'([^C]|c)hapter~\\ref':["CAPITALIZE C IN CHAPTER", 'c', capitalizeChapter],
            r'([^S]|s)ection~\\ref':["CAPITALIZE S IN SECTION", 'c', capitalizeSection],
            r'\\section|\\chapter':["TITLE CASE FOR SECTIONS AND CHAPTERS", 'c', convertToTitleCase],
            r'\\(sub)+section':["ONLY FIRST WORD CAPITALIZED IN SUBSECTIONS", 'c', convertFirstLetterToCapital],
            r' ( )+':["TOO MANY SPACES", 'tce', removeExtraSpaces],
            r'(?i)([ ]+||^)([a-zA-Z][a-zA-Z ]*)[^a-zA-Z0-9]+\2([ \.,;]|$|)':["REPEATED PHRASE",'i',removeRepeatedPhrase]
            }
