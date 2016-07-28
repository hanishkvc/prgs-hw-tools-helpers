#!/usr/bin/python3
#
# Logic to work with Orcad EXP (Export Property) files
# 2015, HanishKVC
#
# Logic to Update a given field's values in Orcad ExportProperties file
# using another field's value as the key to decide on the update value
#

# Example usages:
# ThisPrg update BOM/MapFile EXPFile
# ThisPrg diff/diff_int OldExpFile NewExpFile
# ThisPrg diff_search/diff_search_int NewFileToCheckLineByLine BaseFileToCheckAgainst
# ThisPrg norm OldFileToNormalize NewFileUsedAsReferenceWrtFieldsToRetainAndSequence

# As can be seen from above, ideally the logic in process_diff should use Old and
# New files the other way round so that diff/diff_int and diff_search/diff_search_int
# can have the same position wrt the NewFile and the Old/BaseFile
# ie currently one loops thro each line in the Old file and tries to diff or match it
# with equivalent line (i.e same line number in normal diff and searched line in search
# mode) in New file. Instead one should loop thro each line in New file and try to diff
# or match it with equivalent line in Old file.


import sys

bDEBUG=False
bUpdateInteractive=False
usedOpenErrors=None
usedOpenErrors='surrogateescape'
usedOpenErrors='replace'

if len(sys.argv) < 4:
  print("update/diff/diff_int/diff_search/diff_search_int/norm MAPFile/OldExpFile/NewFileToCheckLineByLine/OldFileToNormalize TheOtherFile")
  print("While Diffing: use simple diff/diff_int if only properties have changed due to updates/corrections")
  print("While Diffing: use better diff_search/diff_search_int if new components have been added or things removed")
  exit(1)

gdMap = {}
gsMode = sys.argv[1]
gsFile1 = sys.argv[2]
gsFile2 = sys.argv[3]
MODE_UPDATE = "update"
MODE_DIFF = "diff"
MODE_INTERACTIVE = "int"
MODE_SEARCH = "search"
MODE_NORMALIZE = "norm"

FIELDINDEX_PARTREFDESIG = 2

# For MfgPN as key and PCBFootPrint the field being updated
#
# Templates to Generate Suitable BOM
# Item\tQuantity\tReference\tPart\tMfg\tMfgPartNum\tPCBFootPrint
# {Item}\t{Quantity}\t{Reference}\t{Value}\t{MFG}\t{MFG_PN}\t{PCB Footprint}
#
gbCustomUpdateMode = False
sMapSKeyHdr = '"MFG_PN"'
iMapSKey = 5
iMapUVal = 6
iExpSKey = 28
iExpUVal = 37

def map_load(sfMap):
  global gdMap
  print("sfMap={}".format(sfMap))
  if (gbCustomUpdateMode):
    input("DBG: iMapSKey={}, iMapUVal={}".format(iMapSKey,iMapUVal))
  fMap = open(sfMap)
  for lMap in fMap:
    pMap = lMap.split("\t")
    if (bDEBUG):
      print(lMap)
      print(pMap)
      print(len(pMap))
    try:
      sSKey = pMap[iMapSKey].strip()
      sUVal = pMap[iMapUVal].strip()
      print("{}={}".format(sSKey,sUVal))
      gdMap[sSKey] = sUVal
    except IndexError:
      if (bDEBUG):
        input("IndexError")

def map_info():
  print("INFO: Total Mappings from SKey to UVal is {}".format(len(gdMap)))

def write_tabbedstrarray(fWExp,pExp):
  bFirst = True
  for c in pExp:
    if (bFirst):
      bFirst = False
      myStr = "{}"
    else:
      myStr = "\t{}"
    fWExp.write(myStr.format(c.strip()))
  fWExp.write("\n")

def write_line(fWExp, lExp):
  print("{}=>{}".format(len(lExp),lExp))
  tlExp = lExp.rstrip("\r")
  lExp = tlExp.rstrip("\n")
  fWExp.write(lExp)
  print("{}=>{}".format(len(lExp),lExp))
  #exit()
  fWExp.write("\n")

def exp_proc(sfExp):
  global gdMap
  iKeyFound=0
  iKeyMissing=0
  iIndexError=0
  iStartLinesOr=0
  print("sfExp={}".format(sfExp))
  if (gbCustomUpdateMode):
    input("DBG: sMapSKeyHdr={}, iExpSKey={}, iExpUVal={}".format(sMapSKeyHdr,iExpSKey,iExpUVal))
  fExp = open(sfExp, newline='\r\n')
  fWExp = open("{}.NEW".format(sfExp),"w+", newline='\r\n')
  for lExp in fExp:
    pExp = lExp.split("\t")
    if (bDEBUG):
      print(lExp)
      print(pExp)
      print(len(pExp))
    try:
      sSKey = pExp[iExpSKey].strip()
      sUVal = pExp[iExpUVal].strip()
      print("Cur:{}={}".format(sSKey,sUVal))
      if ((sSKey == sMapSKeyHdr) or (sSKey == '')):
        iStartLinesOr += 1
        if ((gbCustomUpdateMode) and (sSKey == sMapSKeyHdr)):
          input("DBG: Hdr: iExpSKey={}, iExpUVal={}".format(pExp[iExpSKey],pExp[iExpUVal]))
        #write_line(fWExp,lExp)
        write_tabbedstrarray(fWExp,pExp)
        continue
      try:
        sStrippedSKey = sSKey.strip('"')
        pExp[iExpUVal] = '"{}"'.format(gdMap[sStrippedSKey])
        sNUVal = pExp[iExpUVal].strip()
        print("New:{}={}".format(sSKey,sNUVal))
        iKeyFound += 1
        write_tabbedstrarray(fWExp,pExp)
      except KeyError:
        #input("WARN: KeyField {} = {} Missing".format(sMapSKeyHdr,sSKey))
        print("WARN: KeyField {} = {} Missing; RelatedTo {},{}".format(sMapSKeyHdr,sSKey,pExp[0],pExp[2]))
        if (bUpdateInteractive):
          print("TODO: Add interactive update logic here")
        iKeyMissing += 1
        #fWExp.write(lExp)
        write_tabbedstrarray(fWExp,pExp)
    except IndexError:
      iIndexError += 1
      if (bDEBUG):
        input("IndexError")
      #write_line(fWExp,lExp)
      write_tabbedstrarray(fWExp,pExp)
  print("INFO: iKeyFound={} iKeyMissing={} iIndexError={} iStartLinesOr={}".format(iKeyFound,iKeyMissing,iIndexError,iStartLinesOr))


def mode_update(sfMap,sfExp):
  print("MODE: update")

  global gsMode
  global sMapSKeyHdr, iMapSKey, iMapUVal, iExpSKey, iExpUVal
  global gbCustomUpdateMode

  pModes = gsMode.split("__")
  if (len(pModes) == 6):
    gbCustomUpdateMode = True
    print("INFO: CustomUpdateMetaDataProvided MODE")
    sMapSKeyHdr = '"{}"'.format(pModes[1])
    iMapSKey = int(pModes[2])
    iMapUVal = int(pModes[3])
    iExpSKey = int(pModes[4])
    iExpUVal = int(pModes[5])
  else:
    print("INFO: DefaultUpdateMetaDataUsed MODE")

  map_load(sfMap)
  map_info()
  exp_proc(sfExp)



def find_matchingline_infile(fNew, pOld, iSel, iaMatchedLinesInNew):
  fNew.seek(0)
  iLNum = -1
  if (iSel == FIELDINDEX_PARTREFDESIG): # If we are checking out the Component rows
    fNew.readline() # Discard the filename line
    fNew.readline() # Discard the Header line
    iLNum += 2
  for lCur in fNew:
    iLNum += 1
    pCur = lCur.split("\t")
    if (pOld[iSel] == pCur[iSel]):
      iaMatchedLinesInNew.append(iLNum)
      return lCur
  return None



def process_diff(sfOld, sfNew, bInteractive, bSearch):
  print("sfOld={}".format(sfOld))
  print("sfNew={}".format(sfNew))
  fOld = open(sfOld, newline='\r\n', errors=usedOpenErrors)
  fNew = open(sfNew, newline='\r\n')
  iExtraLinesInNew=0
  iLengthMisMatch=0
  iValueMisMatch=0
  iaMatchedLinesInNew = list()
  iLineNum = -1
  for lOld in fOld:
    iLineNum += 1
    print("\n\nProcessing Line {}\n".format(iLineNum))
    pOld = lOld.split("\t")
    print(pOld)
    print("\n")
    if (bSearch):
      if (iLineNum < 2):
        iSelFld = 1
      else:
        iSelFld = FIELDINDEX_PARTREFDESIG
      lNew = find_matchingline_infile(fNew, pOld, iSelFld, iaMatchedLinesInNew)
      if (lNew == None):
        print("WARN:{}:MissingInfNew[{}]:{},{}".format(iLineNum,sfNew,pOld[0],pOld[iSelFld]))
        if (bInteractive):
          input("PressAnyKey...")
        continue
    else:
      lNew = fNew.readline()
    pNew = lNew.split("\t")
    lenpOld = len(pOld)
    lenpNew = len(pNew)
    if (iLineNum <= 1):
      pHdr = pNew

    print(pNew)
    print("INFO:{}:LengthOf pOld={}, pNew={}".format(iLineNum,lenpOld,lenpNew))

    if (lenpOld != lenpNew):
      iLengthMisMatch += 1
      print("WARN:{}:LengthMisMatchInLine".format(iLineNum))
      if (bInteractive):
        input("PressAnyKey...")
      continue

    for i in range(lenpOld):
      if (not (pOld[i] == pNew[i])):
        iValueMisMatch += 1
        #print("WARN:{}:ValueMisMatch: pHdr[{}]={}: pOld={}, pNew={}".format(iLineNum,i,pHdr[i],pOld[i],pNew[i]))
        print("WARN:{}:ValueMisMatch:{},{}: pHdr[{}]={}: pOld={}, pNew={}".format(iLineNum,pNew[0],pNew[1],i,pHdr[i],pOld[i],pNew[i]))
        if (bInteractive):
          input("PressAnyKey...")
  else:
    print("INFO:Endof fOld reached")
    if (bSearch):
      fNew.seek(0)
      iLNum = -1
      for lNew in fNew:
        iLNum += 1
        try:
          iaMatchedLinesInNew.index(iLNum)
        except ValueError:
          print("WARN:NOTUsedInOld:{}:{}".format(iLNum,lNew))
          if (bInteractive):
            input("PressAnyKey...")
    else:
      for lNew in fNew:
        iExtraLinesInNew += 1
        print("WARN:ExtraLinesInfNew:{}".format(lNew))

  print("NOTE: iLineNum={}, iExtraLinesInNew={}, iLengthMisMatch={}, iValueMisMatch={}".format(iLineNum,iExtraLinesInNew,iLengthMisMatch,iValueMisMatch))


def mode_diff(sfOld,sfNew):
  global gsMode
  bInteractive = False
  bSearch = False
  pModes = gsMode.split("_")
  for cMode in pModes:
    if (cMode == MODE_DIFF):
      print("MODE: diff")
    elif (cMode == MODE_INTERACTIVE):
      print("MODE: diff interactive")
      bInteractive = True
    elif (cMode == MODE_SEARCH):
      print("MODE: diff search")
      bSearch = True
    else:
      print("MODE: diff Unknown, Quiting...")
      exit()
  process_diff(sfOld,sfNew,bInteractive,bSearch)


def write_tabbedstrarray_reordered(fW,pData,iaReOrder):
  for i in range(len(iaReOrder)):
    if (i == 0):
      myStr = "{}"
    else:
      myStr = "\t{}"
    iIndex = iaReOrder[i]
    if (iIndex != -1):
      c = pData[iaReOrder[i]]
    else:
      c = '"<null>"'
    fW.write(myStr.format(c.strip()))
  fW.write("\n")


def process_normalize(sfOld,sfNew):
  print("MODE: Normalize")
  print("sfOld={}".format(sfOld))
  print("sfNew={}".format(sfNew))
  fOld = open(sfOld, newline='\r\n')
  fNew = open(sfNew, newline='\r\n')
  fWOld = open("{}.NORM".format(sfOld),"w+", newline='\r\n')

  # Pass 1st line
  tlOld = fOld.readline()
  fWOld.write(tlOld)
  fNew.readline()
  # Get header line
  lOldHdr = fOld.readline()
  lNewHdr = fNew.readline()
  pOldHdr = lOldHdr.split("\t")
  pNewHdr = lNewHdr.split("\t")

  iaReOrderOld = list()
  bMissing = False
  for fldNew in pNewHdr:
    try:
      oldsNewIndex=pOldHdr.index(fldNew)
      print("INFO:{} located at index {}".format(fldNew,oldsNewIndex))
      iaReOrderOld.append(oldsNewIndex)
    except ValueError:
      bMissing = True
      print("WARN:{} missing in {}".format(fldNew,sfOld))
      iaReOrderOld.append(-1)
  print("INFO:NumOf FieldsInOld={}, FieldsInNew={}".format(len(pOldHdr),len(pNewHdr)))
  if (bMissing):
    sGot = input("INFO:FieldsMissing: Some of fields in {} missing from {}, so Quit Or Continue  with <null> for missing fields...".format(sfNew,sfOld))
    if (sGot.upper() != "CONTINUE"):
      print("Quiting...")
      exit()
    else:
      print("Continuing...")
  write_tabbedstrarray_reordered(fWOld,pOldHdr,iaReOrderOld)

  for lOld in fOld:
    pOld = lOld.split("\t")
    write_tabbedstrarray_reordered(fWOld,pOld,iaReOrderOld)

def mode_normalize(sfOld,sfNew):
  process_normalize(sfOld,sfNew)



if gsMode.startswith(MODE_UPDATE):
  mode_update(gsFile1,gsFile2)
elif gsMode.startswith(MODE_DIFF):
  mode_diff(gsFile1,gsFile2)
elif gsMode == MODE_NORMALIZE:
  mode_normalize(gsFile1, gsFile2)
else:
  print("ERROR:UNKnown Mode, Quiting...")

