'''
Created on Feb 24, 2015

@author: joro
'''
import unittest
from Utilz import readListOfListTextFile

class TestUtilz(unittest.TestCase):
    def testReadListOfListTextFile(self):
        URIfile = '04_Hamiyet_Yuceses_-_Bakmiyor_Cesm-i_Siyah_Feryade_1_zemin_from_11_593270_to_22_910647.phrasesDurationSynthAligned'
        detectedTokenList = readListOfListTextFile(URIfile)
        print detectedTokenList
        #TODO: compare with expected result

if __name__=="__main__":
    test_utilz = TestUtilz()
    test_utilz.testReadListOfListTextFile()
        