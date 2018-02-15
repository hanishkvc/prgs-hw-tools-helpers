#!/bin/env python3

import sys
import os


PCB2Layer = [
    [
        ["drl.rpt", "Drill Report"],
        ["drl", "Drill data"],
        ["drl_map.gbr", "Drill Map"],
    ],
    [
        ["Dwgs.User.gbr", "Board measurements"],
        ["Edge.Cuts.gbr", "Board outline"],
    ],
    [
        ["F.Fab.gbr", "Top Fabrication support layer"],
        ["F.SilkS.gbr", "Top Silk screen"],
        ["F.Paste.gbr", "Top Solder Paste"],
        ["F.Mask.gbr", "Top Solder Mask"],
        ["F.Cu.gbr", "Top Copper"],
        ["B.Cu.gbr", "Bottom Copper"],
        ["B.Mask.gbr", "Bottom Solder Mask"],
        ["B.Paste.gbr" "Bottom Solder Paste"],
        ["B.SilkS.gbr", "Bottom Silk screen"],
        ["B.Fab.gbr", "Bottom Fabrication support layer"],
    ],
    [
        ["top.pos", "Top component placement positions"],
        ["bottom.pos", "Bottom component placement positions"],
    ]
]


def rename_gerber_files(pcb, fl):

    iG = 0
    for g in pcb:
        iI = 0
        for i in g:
            for f in fl:
                if f.endswith(i[0]):
                    curGroup = iG
                    curIndividual = iI
                    curFile = f
                    newFile = "{:02}-{:02}-{}".format(curGroup, curIndividual, curFile)
                    cmd = "mv {} {}".format(curFile, newFile)
                    print("{} is {}".format(newFile, i[1]))
                    #print(cmd)
                    os.system(cmd)

            iI += 1
        iG += 1
        print()



relfiles = { 
        "sch": [ "*.pro", "*.sch", "*.bom.txt", "*.lib", "*.dcm" ],
        "pcb": [ "*.kicad_pcb", "*.pretty" ],
        "gerber": [ "gerber/*" ],
        }

reldest = {
        "sch": "release",
        "pcb": "release",
        "gerber": "release/gerber"
        }

def release(type):
    os.system("mkdir {}".format(reldest[type]))
    for f in relfiles[type]:
        cmd = "cp -a {} {}/".format(f, reldest[type])
        print(cmd)
        os.system(cmd)

if (sys.argv[1] == "release"):
    release(sys.argv[2])

if (sys.argv[1] == "rename_gerber_files"):
    rename_gerber_files(PCB2Layer, sys.argv[2:])

