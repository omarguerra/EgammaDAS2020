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
import math

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection

import EgammaUser.EgammaDAS2020.CoreTools as CoreTools


""" 
Setups up Nano for reading
"""

def cal_dphi(phi1,phi2):
    dphi = phi1-phi2
    while dphi<-math.pi:
        dphi+=2*math.pi
    while dphi>math.pi:
        dphi-=2*math.pi
    return dphi
        
def cal_delta_r2(eta1,phi1,eta2,phi2):
    dphi = cal_dphi(phi1,phi2)
    deta = eta1-eta2
    return deta*deta + dphi*dphi

def pass_filter(ele,trig_objs,filter_nr,max_dr=0.1):
    max_dr2 = max_dr*max_dr
    for trig_obj in trig_objs:
        if (trig_obj.id ==11 and 
            cal_delta_r2(ele.eta+ele.deltaEtaSC,ele.phi,trig_obj.eta,trig_obj.phi) < max_dr2 and
            (trig_obj.filterBits & (0x1 << filter_nr) ) !=0 ):
            return True
    return False
                  
if __name__ == "__main__":


    #now read the cmd line to find our input filename
    #local file "file:<filename>
    #remote file "root:// 
    #note unlike CMSSW proper its not smart enough to resolve to fall over to xrootd automatically
    #so it has to be specified
    parser = argparse.ArgumentParser(description='prints E/gamma pat::Electrons/Photons')
    parser.add_argument('in_filenames',nargs="+",help='input filenames')
    parser.add_argument('--prefix','-p',default='',help='file prefix')
    args = parser.parse_args()

    in_filenames_with_prefix = CoreTools.get_filenames(args.in_filenames,args.prefix)

    Events = ROOT.TChain("Events","chain");
    for x in in_filenames_with_prefix:
        print("adding {}".format(x))
        Events.Add(x)
    nr_events = Events.GetEntries()
    
    print("nrEvents: {}".format(nr_events))

    Events.GetEntry(0)
    eles = Collection(Events,"Electron")
    trig_objs = Collection(Events,"TrigObj")

    
    
    
    
