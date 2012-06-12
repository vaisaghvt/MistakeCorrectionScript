import itertools as it
import re
import os
import Getch as gc
from patterns import * 
from extractPhrases import *
from tagChecks import *
import sys

def dealWithIt(match, para, replacementFunction):
    replacement =  suggestReplacement(match, para, replacementFunction)
    while True:
        print "Suggested replacement:",replacement
        print "(a)ccept suggestion | (i)gnore:",
        option = gc.getch()
        print option
        if option == 'a':
            return replacement, True
        # elif option == 'e':
        #     print "code to edit and write own correction here"
        #     return getReplacement(match, para)
        elif option == 'i':
            print "ignored... "
            return para, False
        else :
            print "invalid choice"

def suggestReplacement(match, para, replacementFunction):
    return replacementFunction(match, para)

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
for fileName in sys.argv[1:]:
    print "//////////////Checking ", fileName, "/////////////////////"
    print "********************"
    group = []
    with open(fileName) as f:
        paras = paragraphs(f)
        for para in paras:
            group.append(para)
    count=0
    # print group
    newContent =""
    matched = False
    for iteration in range(1,3,1):
        for pattern in patterns.keys():
            # print count 
            count=count+1
            flag = False
            for index, para in enumerate(group):
                regex = re.compile(pattern)
                # m = re.findall(pattern,line)
            #   writeFile.write(line.replace("tutu","random"))
                replaced = True
                while (replaced):
                    if replaced:
                        replaced = False;
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
                        group[index], replaced = dealWithIt(match, para, patterns[pattern][2])
                        para= group[index]            
                        print "**********************"
                        if replaced:
                            break
    if matched == False:
        print "No mistakes found. Good Stuff!"
    else:
        print "Corrections made in ", fileName
        writeToFile(group)
        matched = False





    