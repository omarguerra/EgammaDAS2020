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
from Analysis.HLTAnalyserPy.EvtData import EvtData, EvtHandles, add_product

import Analysis.HLTAnalyserPy.CoreTools as CoreTools
import Analysis.HLTAnalyserPy.GenTools as GenTools
import Analysis.HLTAnalyserPy.HistTools as HistTools

""" 
This is an example of how to access E/gamma objects in the MiniAOD in fwlite. 
It uses a simple package developed to ease the usage of fwlite
Its actually for HLT analysis but works well in general

"""


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
    parser.add_argument('--out','-o',default="output.root",help='output filename')
    args = parser.parse_args()
    
    in_filenames_with_prefix = ['{}{}'.format(args.prefix,x) for x in args.in_filenames]

    #this is a handy class we have made which manages all the handles and labels needed to access products
    #it gets the products on demand so its fine in this case to declare products you wont use
    products = [] 
    add_product(products,"eles","std::vector<pat::Electron>","slimmedElectrons")
    add_product(products,"phos","std::vector<pat::Photon>","slimmedPhotons")
    evtdata = EvtData(products,verbose=True)

    #now open the output root file
    out_file = ROOT.TFile(args.out,"RECREATE")
    #create a histogram
    ROOT.sigmaIEtaIEtaHist = ROOT.TH1D("sigmaIEtaIEtaHist",";#sigma_{i#etai#eta};#entries;",100,0,0.03)
    
    events = Events(in_filenames_with_prefix)
    nr_events = events.size()
    for event_nr,event in enumerate(events):
        if event_nr%500==0:
            print("processing event {} / {}".format(event_nr,nr_events))
        evtdata.get_handles(event)
        for ele in evtdata.get("eles"):
            #we will plot this for 20 GeV barrel electrons in our example
            #note we use supercluster eta to for geometric cuts as its from 0,0,0 and therefore represents the detector coordinates
            #electron eta is used for physics quantities as it is w.r.t to the vtx position of the electron and just represents its true eta
            #summary: SC eta = detector eta, electron eta = physics eta
            if ele.et()>20 and abs(ele.superCluster().eta())<1.4442:
                ROOT.sigmaIEtaIEtaHist.Fill(ele.full5x5_sigmaIetaIeta())
                
    out_file.Write()
    
    



