#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import argparse
import ROOT

""" 
This script prints out the availible information in the nano
"""

    

if __name__ == "__main__":

    #now read the cmd line to find our input filename
    #local file "file:<filename>
    #remote file "root:// 
    #note unlike CMSSW proper its not smart enough to resolve to fall over to xrootd automatically
    #so it has to be specified
    parser = argparse.ArgumentParser(description='prints E/gamma pat::Electrons/Photons')
    parser.add_argument('in_filename')
    parser.add_argument('--pattern','-p',default="",help='will print any branch containing this str')
    parser.add_argument('--show_trig','-t',action='store_true',help="will show the L1 & HLT info")
    args = parser.parse_args()

    in_file = ROOT.TFile(args.in_filename,"READ")
    nanotree = in_file.Events

    print("printing nano content")
    for branch in nanotree.GetListOfBranches():
        is_trig = branch.GetName().startswith("L1_") or branch.GetName().startswith("HLT_")
        #is_trig = branch.GetTitle()=="Trigger/flag bit" (alternative way, also kills flags)
        if branch.GetName().find(args.pattern)!=-1 and (not is_trig or args.show_trig):
            print("{}:\n   {}".format(branch.GetName(),branch.GetTitle()))
 
