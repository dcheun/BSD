#!/usr/bin/env python

"""DAT Analyzer.

DATAnalyzer reads in a DAT file and analyzes it for errors.
A report is printed after the analysis.

@deprecated: See qc.py module.

@author:     Danny Cheun
@copyright:  2014 Danny Cheun and Blackstone Discovery.
             Proprietary software.
@contact:    dcheun@gmail.com

"""

import re
import sys

# Export on *
__all__ = ['DATAnalyzer']




def get_column_index(columns):
    """Creates a fields dictionary containing info about
    field name and it's column number.
    
    @param columns: A list containing the column (field) headers in order.
    @return: The dictionary in the form: field_name -> column_number.
    
    """
    # Zip the list with the range into a dictionary.
    return dict(zip(columns, range(0,len(columns))))


# Argument handler.
dat_file = sys.argv[1]
#test file, use above line for proper command line functioning
#file = '/home/odamobi/BSD/ABC001.dat'

with open(dat_file) as f:
    # Strip the '\x00' prefix from the raw data.
    content = [x.replace('\x00','') for x in f.readlines()]

print 'There are ' + str(len(content)) + ' lines in ' + dat_file

numberOfFiles = 0;

missingCustodian = 0
missingNative = 0
missingText = 0
duplicateControlNumber = 0

brokenFamilyError = 0
missingHashError = 0

begDocIndex = 0
custodianIndex = 0
familyIndex = 0
hashValueIndex = 0
nativeIndex = 0
ocrIndex = 0

fieldsDetected = False

# Assume the first row is the column/field headers.
# Create the list as well as stripping some unneeded separators.
clean_list = [re.sub('\xff|\xfe','',x).strip() for x in content[0].split('\xfe\x14\xfe')]
fields = get_column_index(clean_list)
#print fields
#print 'AttRange is in column number %s' % fields.get('AttRange') 

for line in content[0:]:
#  print re.sub('\x00\xfe', ' || ', re.sub('\x00\xfe\x00\x14\x00\xfe', ' | ', line))
#  l = line.split('\x00\xfe\x00\x14\x00\xfe')
  l = [re.sub('\xff|\xfe','',x) for x in line.split('\xfe\x14\xfe')]
  
#  print len(l)
  if not fieldsDetected:
    index = 0
    for i in l:
      #replace null bits with blanks to enable normal ascii searching
      iASCII = i.replace('\x00', '')
      
      #LAW Detection
      if re.search('begDoc', iASCII, re.IGNORECASE):
        begDocIndex = l.index(i)
      
      if re.search('AttRange', iASCII, re.IGNORECASE):
        familyIndex = l.index(i)

      if re.search('Custodian', iASCII, re.IGNORECASE):
        custodianIndex = l.index(i)

      if re.search('MD5Hash', iASCII, re.IGNORECASE):
        hashValueIndex = l.index(i)

      if re.search('NativeFile', iASCII, re.IGNORECASE):
        nativeIndex = l.index(i)
        
      if re.search('OCRPath', iASCII, re.IGNORECASE):
        ocrIndex = l.index(i) 
        
      #EDA Detection
      if re.search('ATTACHRANGE', iASCII, re.IGNORECASE):
        familyIndex = l.index(i)
      
#     sys.stdout.write("Index " + str(index) + ": ")
#     sys.stdout.write("[" + i + "]\n")
#      index = index + 1
    fieldsDetected = True
    continue

## test INDEX DETERMINATION CODE
  #print '\n==== START LINE ======'
  #index = 0
  #for i in l:
    #sys.stdout.write("Index " + str(index) + ": ")
    #sys.stdout.write("[" + i + "]\n")
    #index = index + 1
  #print '\n==== END LINE ======'
  errorPresent = False
  
  # Only process line if the number of fields are expected.
#  if len(l) == 46:
  if len(l) == len(fields):
    numberOfFiles += 1
#    for i in l:
#   LAW DETECTION
    if 'AttRange' in fields and l[fields['AttRange']]:
#      print '.' + l[4] + '.' + str(len(l[4]))
      if not re.search(r'.+-.+', l[familyIndex], re.IGNORECASE):
        brokenFamilyError += 1
        sys.stdout.write("*ERROR DETECTED: BROKEN FAMILY*\n")
        errorPresent = True
           
#   LAW Detection
    if 'Custodian' in fields and len(l[fields['Custodian']]) < 2:
      missingCustodian += 1
      sys.stdout.write("*ERROR DETECTED: MISSING CUSTODIAN*\n")
      errorPresent = True
        
    if 'MD5Hash' in fields and len(l[fields['MD5Hash']]) < 5:
      missingHashError += 1
      sys.stdout.write("*ERROR DETECTED: MISSING HASH VALUE*\n")
      errorPresent = True

    if 'NativeFile' in fields and len(l[fields['NativeFile']]) < 5:
      missingNative += 1
      sys.stdout.write("*ERROR DETECTED: MISSING NATIVE*\n")
      errorPresent = True

    if 'OCRPath' in fields and len(l[fields['OCRPath']]) < 10:
      missingText += 1
      sys.stdout.write("*ERROR DETECTED: MISSING OCR TEXT*\n")
      errorPresent = True

#   EDA Detection
    if 'CUSTODIAN' in fields and len(l[fields['CUSTODIAN']]) < 2:
      missingCustodian += 1
      sys.stdout.write("*ERROR DETECTED: MISSING CUSTODIAN*\n")
      errorPresent = True
        
    if 'MD5HASH' in fields and len(l[fields['MD5HASH']]) < 5:
      missingHashError += 1
      sys.stdout.write("*ERROR DETECTED: MISSING HASH VALUE*\n")
      errorPresent = True

    if 'NATIVEFILE' in fields and len(l[fields['NATIVEFILE']]) < 5:
      missingNative += 1
      sys.stdout.write("*ERROR DETECTED: MISSING NATIVE*\n")
      errorPresent = True

    if 'TEXTPATH' in fields and len(l[fields['TEXTPATH']]) < 10:
      missingText += 1
      sys.stdout.write("*ERROR DETECTED: MISSING TEXT*\n")
      errorPresent = True

    if errorPresent:
      print '==== START LINE ======'
      for i in l:
        sys.stdout.write(i + ' | ')
      print '==== END LINE ======\n'


print "\n**DAT FILE INFORMATION:**\n"
print "Number of Files: " + str(numberOfFiles)
print "\n**ISSUES**\n"
print "Missing Natives: " + str(missingNative)
print "Missing Text: " + str(missingText)
print "Missing Hash Value: " + str(missingHashError)
print "Broken Families: " + str(brokenFamilyError)
print "Missing Custodians: " + str(missingCustodian)
#print "clean_list: \n"
#for i in clean_list:
#  sys.stdout.write(i + ' | ')

def main():
    pass

if __name__ == '__main__':
    main()

