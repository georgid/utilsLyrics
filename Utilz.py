'''
Created on Mar 12, 2014

@author: joro
'''

import codecs
import numpy
import os
import sys

parentDir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0]) ), os.path.pardir)) 
sys.path.append(parentDir)

    ##################################################################################

    ## TODO: callback function to load code. Put it in a different folder
def loadTextFile( pathToFile):
        
        # U means cross-platform  end-line character
        inputFileHandle = codecs.open(pathToFile, 'rU', 'utf-8')
        
        allLines = inputFileHandle.readlines()

        
        inputFileHandle.close()
        
        return allLines


##################################################################################
def writeListOfListToTextFile(listOfList,headerLine, pathToOutputFile, toFlip=False):    
    outputFileHandle = codecs.open(pathToOutputFile, 'w', 'utf-8')
    
    if not headerLine == None:
        outputFileHandle.write(headerLine)
    
    # flip (transpose) matrix
    if toFlip:
        a = numpy.rot90(listOfList)
        listOfList = numpy.flipud(a)
    
    for listLine in listOfList:
        
        output = ""
        for element in listLine:
            outputFileHandle.write("{:35}\t".format(element))
#             output = output + str(element) + "\t"
#         output = output.strip()
#         output = output + '\n'
#         outputFileHandle.write(output)
        outputFileHandle.write('\n')    
    
    outputFileHandle.close()
    
    print "successfully written file: " , pathToOutputFile, "\n"


##################################################################################
def writeTextToTextFile(inputText, pathToOutputFile):    
    outputFileHandle = codecs.open(pathToOutputFile, 'w', 'utf-8')
    
    
    outputFileHandle.write(inputText)
    
    outputFileHandle.close()




##################################################################################
def writeListToTextFile(inputList,headerLine, pathToOutputFile):    
    outputFileHandle = codecs.open(pathToOutputFile, 'w', 'utf-8')
    
    if not headerLine == None:
        outputFileHandle.write(headerLine)
    
    for listLine in inputList:
        listLine = str(listLine) + '\n'
        outputFileHandle.write(listLine)
    
    outputFileHandle.close()
    print "successfully written file: " , pathToOutputFile, "\n"



    
    
    ########### statistics on a array
def getMeanAndStDevError(alignmentErrors):
        
        absalignmentErrors = [0] * len(alignmentErrors)
        for index, alError in enumerate(alignmentErrors):
            absalignmentErrors[index] = abs(alError)
        
        mean = numpy.round(numpy.mean(absalignmentErrors), decimals=2)
        median = numpy.round( numpy.median(absalignmentErrors), decimals=2)
        stDev = numpy.round( numpy.std(alignmentErrors), decimals=2)
        
        return mean, stDev, median
    
    
def getSectionNumberFromName(URIrecordingNoExt):
    '''
    infer which section number form score is needed by the *_2_meyan_* in the file name
    '''
    underScoreTokens  = URIrecordingNoExt.split("_")
    index = -1
    while (-1 * index) <= len(underScoreTokens):
        token = str(underScoreTokens[index])
        if token.startswith('meyan') or token.startswith('zemin') or \
        token.startswith('nakarat'):
            break
        index -=1
    
    try:
        whichSection = underScoreTokens[index-1]
    except Exception:
        sys.exit("please put the number of section before its name: e.g. *_2_meyan_* in the file name ")
    return int(whichSection)

    
    