#!/bin/env python3
# Generate BOM (csv) from KiCAD XML metadata file
# HanishKVC, v20170320
# 201X, GPL
#

import sys
import xml.etree.ElementTree as ET

bDEBUG=False
tagDESIGN = "design"
tagSHEET = "sheet"
tagTITLEBLOCK = "title_block"
tagCOMPONENTS = "components"
tagFIELDS = "fields"

# This is the list of directly (natively) supported properties
requiredProps = [ 'value', 'footprint' ]
# This is the list of user define properties for the components
requiredFields = [ 'Mfg' ]
# This is the sequence in which the properties should be dumped into the BOM file
bomDataOrder = [ 'ref', 'value', 'footprint', 'Mfg' ]


def dprint(*args):
    if (not bDEBUG):
        return
    for c in args:
        print(c, end="")
    print("")

root=ET.parse(sys.argv[1]).getroot()
aMetaData = []
aComponents = []
for cR in root:
    dprint(cR.tag, cR.attrib)
    if (cR.tag == tagDESIGN):
        print("***TITLE***")
        for cData in cR:
            dprint(cData.tag, cData.attrib)
            if (cData.tag == tagSHEET) and (cData.attrib['number'] == "1"):
                for cDataL2 in cData:
                    if (cDataL2.tag == tagTITLEBLOCK):
                        for cMetaData in cDataL2:
                            if (cMetaData.text == None):
                                continue
                            dprint(cMetaData.tag, cMetaData.text)
                            aMetaData.append("{}:{}".format(cMetaData.tag, cMetaData.text))
    if (cR.tag == tagCOMPONENTS):
        print("***COMPONENTS***")
        for cComp in cR:
            component = {}
            dprint(cComp.tag, cComp.attrib)
            component['ref'] = cComp.attrib['ref']
            cFields = None
            for cProp in cComp:
                dprint(cProp.tag, cProp.attrib, cProp.text)
                if (cProp.tag == tagFIELDS):
                    cFields = cProp
                try:
                    tFindProp = requiredProps.index(cProp.tag)
                    component[cProp.tag] = cProp.text
                except:
                    pass
            if (cFields != None):
                for cField in cFields:
                    try:
                        tFindField = requiredFields.index(cField.attrib['name'])
                        component[cField.attrib['name']] = cField.text
                    except:
                        pass

            aComponents.append(component)

#print(aComponents)

def print_line(fOut, lData):
    iLen = len(bomDataOrder)
    iCur = 0
    for c in lData:
        iCur += 1
        if (iCur == iLen): 
            sFormat="{}"
        else:
            sFormat="{}\t"
        print(sFormat.format(c), file=fOut, end='')
    print("", file=fOut)


# Open the output file or stdout
fOut = None
if len(sys.argv) >= 3:
    fOut = open("{}.csv".format(sys.argv[2]),"w+")
else:
    fOut = sys.stdout

# Output metadata
for cMetaData in aMetaData:
    print(cMetaData, file=fOut)

# Output Header
print_line(fOut, bomDataOrder)

# Output component data
for cComp in aComponents:
    lData = []
    for cDataTag in bomDataOrder:
        try:
            lData.append(cComp[cDataTag])
        except:
            lData.append("<NULL>")
        
    print_line(fOut, lData)

if (fOut != sys.stdout):
    fOut.close()



