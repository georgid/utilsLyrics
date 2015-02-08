'''
Created on Mar 12, 2014

@author: joro
'''

import codecs
import numpy
import os
import sys
import difflib
import glob

parentDir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0]) ), os.path.pardir)) 
sys.path.append(parentDir)

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

    ##################################################################################


def findFileByExtensions(pathToComposition, listExtensions):
    '''
    @return: name (with no dir) of first found file 
    '''
    
#     listExtensions = ["sections.txt", "sections.tsv", "sections.json"]
    if not listExtensions:
        sys.exit("{} is empty".format(listExtensions))

    os.chdir(pathToComposition)

    sectionFiles = glob.glob("*." + listExtensions[0])
    if not sectionFiles:
        sectionFiles = glob.glob("*." + listExtensions[1])
        if not sectionFiles:
                sectionFiles = glob.glob("*." + listExtensions[2])
    return sectionFiles


def matchSections(s1, s2, indicesS2):
    '''
    MAtch automatically the section names in s2 to these in s1. 
    @param indicesS2: for each lelement in s2 -> to which element in s1 corresponds: give it empty. 
    @return:  the inidices for s2 indicating the matched sections in s1 
    '''
  
    for (i,a) in enumerate(s1):
        s1[i]= s1[i].lower()
    for (i,a) in enumerate(s2):
        s2[i]= s2[i].lower()
     
    matcher = difflib.SequenceMatcher(None,s1,s2)

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            print 'The sections [%d:%d] of s1 and [%d:%d] of s2 are the same' % \
                (i1, i2, j1, j2)
            for c in range(i1,i2):
                indicesS2.append(c)

        elif tag == 'insert':
            print 'Insert %s from [%d:%d] of s2 into s1 at %d' % \
                (s2[j1:j2], j1, j2, i1)
            indicesS2 = matchSections(s1,s2[j1:j2], indicesS2)

        # section not present in score
        elif tag == 'replace':
            print '{} replaced with {}. add -1 because not present in score'.format( s1[i1:i2], s2[j1:j2])
            for c in range(j1,j2):
                indicesS2.append(-1) 
           
    return indicesS2
            
    
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
    
    logger.info( "successfully written file: " , pathToOutputFile, "\n")


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
    logger.info ("successfully written file: " , pathToOutputFile, "\n")



    
    
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
        if token.startswith('meyan') or token.startswith('zemin') or   token.startswith('gazel') or \
        token.startswith('nakarat') or token.startswith('aranagme') or  token.startswith('taksim')  :
            break
        index -=1
    
    try:
        whichSection = underScoreTokens[index-1]
    except Exception:
        sys.exit("please put the number of section before its name: e.g. *_2_meyan_* in the file name ")
    return int(whichSection)


def renameFilesInDir(argv):
    '''
    renameSectionIndices in a dir with extension e.g. TextGrid
    use method renameSectionIndex
    '''
    if len(argv) != 3:
        sys.exit("usage: {} <dirURI> <extension>".format(argv[0]))
    
    dirURI = argv[1]
    extension = argv[2]
    listExtensions = [extension]

    fileNames = findFileByExtensions(dirURI, listExtensions)
    
    for fileName in fileNames:
        fileURI = os.path.join(dirURI, fileName)
        renameSectionIndex(fileURI)
        
    
    
# rename
    
    

def renameSectionIndex(URIrecording):
    '''
    rename. change number of score section to another number. Needed if score sections are renumbered in sections.tsv/json file/
    NOTE: could be changed for other renaming purposes accordingly 
    '''
    underScoreTokens  = URIrecording.split("_")
    index = -1
    found = False
#     check array in reverse order 
    while (-1 * index) <= len(underScoreTokens):
        token = str(underScoreTokens[index])
        if token.startswith('meyan') or token.startswith('zemin') or   token.startswith('gazel') or \
        token.startswith('nakarat') or token.startswith('aranagme') or  token.startswith('taksim')  :
            found = True
            break
        # decrement
        index -= 1
    if not found:
        sys.exit("please put the number of section before its name: e.g. *_2_meyan_* in the file name ") 
    
    print index
    sectionIndex = int(underScoreTokens[index-1]) 
    sectionIndex += 1
    underScoreTokens[index-1] = str(sectionIndex)
    newURIrecording = "_".join(underScoreTokens)
    print newURIrecording
    
    try:
        os.rename(URIrecording, newURIrecording)
        logger.warn("renaming {} to {}".format(URIrecording, newURIrecording)) 
    except Exception, error:
        print str(error)


if __name__ == '__main__':
# test some functionality
        renameFilesInDir(sys.argv)