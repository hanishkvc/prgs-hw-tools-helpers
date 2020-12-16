###################
Hw Tools Helpers
###################
HanishKVC, 20XYs


Orcard related Helpers
########################

Exp file util
================

THis is very useful to when creating or working with large schematics spanning
over many 10s of pages. Equally for simple projects / schematics also it can be 
used to track or verify changes and or update things or so, along with a easy
to look at or study or process or ...  textual paper trail.


Updating properties
**********************

cmd: update BOM/MapFile EXPFile

Update a given field's value in Orcad ExportProperties file by using
another field(of that component)'s value as the key into a database
and getting the updated value to use.

Usecase: After one creates and or decides to change the PCBFootprint
associated with a component, to update the same into the schematic,
if the component is used a lot, then

1. create a map file
   * could be a simple csv file containing the MfgPartNumber
     and the new PCBFootprint name
   * or could be the BOM file updated with the new MfgPartNumber
2. export the properties file
3. run this program in update mode
4. if you want to, run this program in diff mode to cross verify the
   updates/changes.
5. import the properties file

UseCase: Similarly if one decides to change the value of one or more
components used in many places, then this can be used to execute the
changes in a controlled and for sure manner.


Comparing/Diffing between Schematic revisions
***********************************************

As orcard doesnt have a builtin change tracking logic. this can be used to
check the differences between schematic revisions. ie instead of trying to
look through the schematic visually (wont help identify non visible property
changes) or wade through a long BOM or worse still EXP file.

NOTE: _int suffix means interactive, where for each change/difference found
the program pauses.

NOTE: the simple diff is simple minded in its comparision, while the diff_search
tries to be bit more exhaustive and or make it easy for the user by trying to
dig out the needles from the hay stack ;-)

Property changes only
------------------------

If one has changed some properties due to updates/corrections, and inturn wants
to cross verify the same in a simple and for sure manner (instead of going thro
the gui or the exportprops/bom file manually) then use the simpler diff command.

cmd: diff/diff_int OldExpFile NewExpFile

Even Additions or Deletions
-----------------------------

If one has also added or removed components, in addition to changing properties,
then use

cmd: diff_search/diff_search_int NewFileToCheckLineByLine BaseFileToCheckAgainst

It will not only help find the differences in properties of the components, or
if required even position changes. It will also show the list of components that
have been added and or removed. Thus making it easy to understand the difference
between the revisions.


Prepare Exp file for use
**************************

Working with a Very Old Revision

  Sometimes over the life of a design, either properties get added or removed
  or the tool decides to change things around or so. While the core set of props
  generally remain the same and logically consistent. When one wants to compare
  a very old revision of a design with a newer or latest revision, with such
  changes inbetween them, then running the previously mentioned diff commands
  directly will lead to too many changes being flagged.

Interested in only a subset of properties

  To keep things simple, we may be interested in tracking only a subset of the
  properties or so and not every thing.

In either of the above cases, one can transform the Exp file to get the job done
by using the below command

cmd: norm OldOrTheFileToNormalize NewOrTheFileUsedAsReferenceWrtFieldsToRetainAndSequence

This will generate a new Exp file for use with the diff commands of this program
which is easier to work with for the user.


History
**********

I had created this utility a very long time back and inturn used it and tweaked
it as and when required over the years. As usual I had forgotten to track the
changes and or document it then. What is commited is the version which seems
to have survived as a backup from sometime back.

This readme is being created after a gap of few years now, so it only contains
what I remember now by looking at the begining of the program file now and not
necessarily all the details.


Others
########

KiCad helpers


MISC
######

NOTE: If and when I find other revisions or other of my previous helper utilities,
I may nuke and recreate the git repo to try and follow the history and or to better
structure the things around.

