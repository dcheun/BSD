#!/usr/bin/env python

"""Quality Control module.

qc provides various libraries for quality checking data files,
such as DATAnalyzer.

@author:     Danny Cheun
@copyright:  2014 Danny Cheun and Blackstone Discovery.
             Proprietary software.
@contact:    dcheun@gmail.com

"""

import re
import sys
from textwrap import dedent

# Define what gets exported on *
__all__ = ['DATAnalyzer']


class DATAnalyzer():
    
    """Analyzes a dat file for errors, and provides procedures
    for printing the report of the analysis.
    
    """
    
    _numberOfFiles = 0
    
    _missingCustodian = 0
    _missingNative = 0
    _missingText = 0
    _duplicateControlNumber = 0
    
    _brokenFamilyError = 0
    _missingHashError = 0
    
    _report = ''
    
    _TAG = ''
    
    def __init__(self):
        """Constructs a new DATAnalyzer."""
        self._TAG = self.__class__.__name__
    
    def get_column_index(self, columns):
        """Creates a fields dictionary containing info about
        field name and it's column number.
        
        @param columns: A list containing the column (field) headers in
                order.
        @return: The dictionary in the form: field_name -> column_number.
        
        """
        # Zip the list with the range into a dictionary.
        return dict(zip(columns, range(0,len(columns))))
    
    def analyze(self, _file):
        """Analyzes the file passed in.
        
        @param _file: The file to read and analyze.
        
        """
        with open(_file) as f:
            # Strip the '\x00' prefix from the raw data.
            content = [x.replace('\x00','') for x in f.readlines()]
        
        # Assume the first row is the column/field headers.
        # Create the list as well as stripping some unneeded separators.
        clean_list = [re.sub('\xff|\xfe','',x).strip()
                      for x in content[0].split('\xfe\x14\xfe')]
        fields = self.get_column_index(clean_list)
        
        for line in content[1:]:
            l = [re.sub('\xff|\xfe','',x) for x in line.split('\xfe\x14\xfe')]
            
            # Only process line if the number of fields are expected.
            if len(l) != len(fields):
                continue
            
            errorPresent = False
            self._numberOfFiles += 1

            # LAW DETECTION
            if 'AttRange' in fields and l[fields['AttRange']]:
                if not re.search(r'.+-.+', l[fields['AttRange']],
                                 re.IGNORECASE):
                    self._brokenFamilyError += 1
                    sys.stdout.write("*ERROR DETECTED: BROKEN FAMILY*\n")
                    errorPresent = True
           
            if 'Custodian' in fields and len(l[fields['Custodian']]) < 2:
                self._missingCustodian += 1
                sys.stdout.write("*ERROR DETECTED: MISSING CUSTODIAN*\n")
                errorPresent = True
        
            if 'MD5Hash' in fields and len(l[fields['MD5Hash']]) < 5:
                self._missingHashError += 1
                sys.stdout.write("*ERROR DETECTED: MISSING HASH VALUE*\n")
                errorPresent = True
            
            if 'NativeFile' in fields and len(l[fields['NativeFile']]) < 5:
                self._missingNative += 1
                sys.stdout.write("*ERROR DETECTED: MISSING NATIVE*\n")
                errorPresent = True
            
            if 'OCRPath' in fields and len(l[fields['OCRPath']]) < 10:
                self._missingText += 1
                sys.stdout.write("*ERROR DETECTED: MISSING OCR TEXT*\n")
                errorPresent = True
            
            # EDA Detection
            if 'CUSTODIAN' in fields and len(l[fields['CUSTODIAN']]) < 2:
                self._missingCustodian += 1
                sys.stdout.write("*ERROR DETECTED: MISSING CUSTODIAN*\n")
                errorPresent = True
            
            if 'MD5HASH' in fields and len(l[fields['MD5HASH']]) < 5:
                self._missingHashError += 1
                sys.stdout.write("*ERROR DETECTED: MISSING HASH VALUE*\n")
                errorPresent = True
            
            if 'NATIVEFILE' in fields and len(l[fields['NATIVEFILE']]) < 5:
                self._missingNative += 1
                sys.stdout.write("*ERROR DETECTED: MISSING NATIVE*\n")
                errorPresent = True
            
            if 'TEXTPATH' in fields and len(l[fields['TEXTPATH']]) < 10:
                self._missingText += 1
                print "*ERROR DETECTED: MISSING TEXT*"
                errorPresent = True
            
            if errorPresent:
                print '==== START LINE ======'
                for i in l:
                    sys.stdout.write(i + ' | ')
                print '\n==== END LINE ======\n'
    
    def print_report(self):
        print dedent('''
        **DAT FILE INFORMATION**
        Number of Files: %s 
        
        **ISSUES**
        Missing Natives: %s
        Missing Text: %s
        Missing Hash Value: %s
        Broken Families: %s
        Missing Custodians: %s
        ''' % (self._numberOfFiles, self._missingNative,
               self._missingText, self._missingHashError,
               self._brokenFamilyError, self._missingCustodian))
    
    def __repr__(self):
        return "DATAnalyzer()"
    
    def __str__(self):
        return "DATAnalyzer"


# def main():
#     dat_file = sys.argv[1]
#     analyzer = DATAnalyzer()
#     analyzer.analyze(dat_file)
#     analyzer.print_report()
#  
# if __name__ == '__main__':
#     main()

