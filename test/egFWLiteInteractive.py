#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from array import array
import argparse
import sys
import ROOT
import json
import re
import os

from DataFormats.FWLite import Events, Handle
from EgammaUser.EgammaDAS2020.EvtData import EvtData, EvtHandles, add_product

import EgammaUser.EgammaDAS2020.CoreTools as CoreTools
import EgammaUser.EgammaDAS2020.GenTools as GenTools

""" 
This is an example of how to access E/gamma objects in the MiniAOD in fwlite. 
It uses a simple package developed to ease the usage of fwlite
Its actually for HLT analysis but works well in general

"""

def get_eles(evtdata,events,indx):
    """
    A small helper function to save typing out this commands each time
    """
    events.to(indx)
    evtdata.get_handles(events)
    eles = evtdata.get("eles")
    print("event: {} {} {}".format(events.eventAuxiliary().run(),events.eventAuxiliary().luminosityBlock(),events.eventAuxiliary().event()))
    print("# eles = {}".format(eles.size()))
    return eles
    

if __name__ == "__main__":

    #first we load in the FWLite libaries and enable them 
    CoreTools.load_fwlitelibs()

    #now read the cmd line to find our input filename
    #local file "file:<filename>
    #remote file "root:// 
    #note unlike CMSSW proper its not smart enough to resolve to fall over to xrootd automatically
    #so it has to be specified
    parser = argparse.ArgumentParser(description='prints E/gamma pat::Electrons/Photons')
    parser.add_argument('in_filenames',nargs="+",help='input filenames')
    parser.add_argument('--prefix','-p',default='',help='file prefix')
    args = parser.parse_args()
    
    #this is a handy class we have made which manages all the handles and labels needed to access products
    #it gets the products on demand so its fine in this case to declare products you wont use
    products = [] 
    add_product(products,"eles","std::vector<pat::Electron>","slimmedElectrons")
    add_product(products,"phos","std::vector<pat::Photon>","slimmedPhotons")
    add_product(products,"trigRes","edm::TriggerResults","TriggerResults::HLT")
    evtdata = EvtData(products,verbose=True)

    events = Events(args.in_filenames)
    nr_events = events.size()
    
    print("nrEvents: {}".format(nr_events))

    """
    now we can play around with the electrons interactively, 
    for example to get the electrons of the 3rd event, do
    
    events.to(3)
    evtdata.get_handles(events)
    eles = evtdata.get("eles")
    
    a simply function get_eles() is defined above to simplify this so you can switch events easily
    eles = get_eles(evtdata,events,3)

    note, interactive investigation here is more to help you understand how electrons work 
    in general or look at a specific event, it is not how you do a serious analysis

    ie its great for learning and testing, not so good for analysing
    """
