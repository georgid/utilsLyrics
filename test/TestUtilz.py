'''
Created on Feb 24, 2015

@author: joro
'''
import unittest
from Utilz import readListOfListTextFile, readListOfListTextFile_gen,\
    writeListOfListToTextFile, loadDictFromTabFile, findFilesByExtension
from curses.ascii import NAK

class TestUtilz(unittest.TestCase):
    
    def testReadListOfListTextFile(self):
        '''
        this is a unit test
        '''
        URIfile = '04_Hamiyet_Yuceses_-_Bakmiyor_Cesm-i_Siyah_Feryade_1_zemin_from_11_593270_to_22_910647.phrasesDurationSynthAligned'
        
        detectedTokenList = readListOfListTextFile(URIfile)
        print detectedTokenList
        #TODO: compare with expected result
#         final check not finished
    
def testLoadDictFromTabFile():
        fileURI = 'modelName2FileNameDict'
        dict = loadDictFromTabFile(fileURI)
        print dict
  
def  testFindFilesByExtension():
    
         path ='/Users/joro/Documents/Phd/UPF/JingjuSingingAnnotation/lyrics2audio/praat/'
         findFilesByExtension(path, 'wav')
    

def testReadListOfListTextFile_gen():
        URIfile = '/Users/joro/Downloads/kimseye-annotation-score-to-audio.txt'
        
        shiftedNakarat = []
        
        inNakarat = 0
        detectedTokenList = readListOfListTextFile_gen(URIfile)
        
        
        # get TS 
        for entry in detectedTokenList:
            if entry[3] == 'D5-NAKARAT-n1':
               beginTs = entry[0]
            if entry[3] == 'D5-NAKARAT*-n1':
                endTs = entry[0]
                break
        
        
        endTs = 111.687981859 
        for entry in detectedTokenList:
            if entry[3] == 'D5-NAKARAT-n1':
               inNakarat = 1
            if entry[3] == 'D5-NAKARAT*-n1':
                inNakarat = 0
                break
            
            if inNakarat:
                entry[0] += (endTs - beginTs)
                shiftedNakarat.append(entry)
        
        writeListOfListToTextFile(shiftedNakarat,None, 'shiftedNakarat.txt', toFlip=False)        
               
        
            
            
        print detectedTokenList

if __name__=="__main__":
    
    testFindFilesByExtension()
#     testLoadDictFromTabFile()
#     testReadListOfListTextFile_gen()
    
#     test_utilz = TestUtilz()
#     test_utilz.testReadListOfListTextFile()
        