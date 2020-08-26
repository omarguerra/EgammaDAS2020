#!/usr/bin/env python
from array import array
import argparse
import sys
from DataFormats.FWLite import Events, Handle
import ROOT


""" 
This is an example of how to access E/gamma objects in the MiniAOD in fwlite 

"""


if __name__ == "__main__":

    #first we load in the FWLite libaries and enable them
    ROOT.gSystem.Load("libFWCoreFWLite.so");
    ROOT.gSystem.Load("libDataFormatsFWLite.so");
    ROOT.FWLiteEnabler.enable()

    #now read the cmd line to find our input filename
    #local file "file:<filename>
    #remote file "root:// 
    #note unlike CMSSW proper its not smart enough to resolve to fall over to xrootd automatically
    #so it has to be specified
    parser = argparse.ArgumentParser(description='prints E/gamma pat::Electrons/Photons')
    parser.add_argument('in_filename',help='input filename')
    args = parser.parse_args()
    
    
    #like in the CMSSW framework, products are accessed by handles, hence we need to declare them
    #a handle is for a specific c++ type in our case a std::vector of pat::Electrons or Photons
    #you then need to specify the label which is the name of the product you want to access
    eles_handle, ele_label = Handle("std::vector<pat::Electron>"), "slimmedElectrons"
    phos_handle, pho_label = Handle("std::vector<pat::Photon>"), "slimmedPhotons"

    #this creates the events to be used in the event loop, reading in the information from the files
    events = Events(args.in_filename)

    """
    now you can access the variables of an electron/photon interactively
    
    events.to(0) #go to 1st event in the file
    events.getByLabel(ele_label,eles_handle)
    
    eles_handle.product() = vector of pat::Electrons
    
    plot try plotting some variables 
    eles = eles_handle.product()
    eles[0].energy() #energy of the first electron
    eles[0].full5x5_sigmaIetaIeta() #sigmaIEtaIEta
    help(ele[0]) will give you useful messages
    
    """

    
