# -*- coding: utf-8 -*-
#
#   Reports.Dump_SemanticDomains_To_File
#    - A FlexTools Module -
#
#   Dump the Semantic Domain list in a FLEx database to file.
#
#   Kien-Wei Tseng
#   March 2016
#
#   Platforms: Python .NET and IronPython
#

from FTModuleClass import *
import codecs

#----------------------------------------------------------------
# Documentation that the user sees:

docs = {FTM_Name        : "Dump Semantic Domain List To File",
        FTM_Version     : 1,
        FTM_ModifiesDB  : False,
        FTM_Synopsis    : "Dump the Semantic Domain list to a file.",
        FTM_Description :
u"""
Dump the Semantic Domain list to a file.
""" }
                 
#----------------------------------------------------------------
# The main processing function

def MainFunction(DB, report, modifyAllowed):

    outputFile = "SemanticDomains_{0}.txt".format(DB.db.ProjectId.UiName)
    output = codecs.open(outputFile, mode="w", encoding="utf8")

    count = 0
    for sd in DB.GetAllSemanticDomains(True):
        #output.write(sd.Hvo + '\r\n')
        output.write(sd.ToString())
        output.write('\r\n')
        report.Info("Semantic Domain: %s" % sd)
        count      += 1
    report.Info("Dumped {0} Semantic Domains to file {1}".format(count, outputFile))
    output.close()
         
#----------------------------------------------------------------
# The name 'FlexToolsModule' must be defined like this:

FlexToolsModule = FlexToolsModuleClass(runFunction = MainFunction,
                                       docs = docs)
            
#----------------------------------------------------------------
if __name__ == '__main__':
    FlexToolsModule.Help()
