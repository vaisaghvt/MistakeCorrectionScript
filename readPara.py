import itertools as it
import re
import os
import Getch as gc
from patterns import * 
from extractPhrases import *
from tagChecks import *
import sys

def dealWithIt(match, para, replacementFunction):
    """ Deals with a pattern match. Checks for replacement, displays it for user and asks what to do with 
    it"""
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
    """ Calls the replacement function with the right arguments"""
    return replacementFunction(match, para)

def saveChanges(group):
    """ Saves the changes that are made."""
    # for para in group:
    #     print para  
    tempFileName = fileName+".temp"  
    with open(tempFileName,"w") as writeFile:
        for para in group:
            writeFile.write(para+'\n')
    os.remove(fileName)
    os.rename(tempFileName,fileName)

# write as seperate module
#Also, try to seperate itemize , etc. maybe have another function to slice it further.


# paragraph_lists = []
for fileName in sys.argv[1:]:
    """ Checks for each file passed as argument """
    print "//////////////Checking ", fileName, "/////////////////////"
    print "********************"
    group = []
    with open(fileName) as f:
        """ Generate paragraphs and store in the list group"""
        paras = paragraphs(f)
        for para in paras:
            group.append(para)
    count=0
    # print group
    newContent =""
    matched = False
    for iteration in range(1,3,1):
        """ Iterate twice so that all patterns are checked for. Still no garantuee that all corrections have been 
        made. Since corrections might bring new errors."""
        # print 'outermost loop'
        for pattern in patterns.keys():
            """ Iterates through each given pattern"""
            # print count 
            count=count+1
            flag = False
            # print 'inner loop'
            for index, para in enumerate(group):
                """ Checks each para for that pattern"""
                regex = re.compile(pattern)
                # print 'inner inner loop'
                # m = re.findall(pattern,line)
            #   writeFile.write(line.replace("tutu","random"))
                replaced = True
                while (replaced):
                    """ if replaced then have to do the check again """
                    # print 'inner inner inner loop'
                    if replaced:
                        replaced = False;
                    for match in regex.finditer(para):
                        """ Iterates through all the matches in each para """
                        # print 'matching loop'
                        for option in patterns[pattern][1]:
                            # print 'option check loop'
                            if(checkPattern(option, match, para)):
                                # print 'flag true'
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
        saveChanges(group)
        matched = False





    