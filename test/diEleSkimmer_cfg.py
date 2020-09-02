import FWCore.ParameterSet.Config as cms

process = cms.Process("ZSKIM")
#process = cms.Process("UPDATE")

import FWCore.ParameterSet.VarParsing as VarParsing
options = VarParsing.VarParsing ('analysis') 
options.register('nrThreads',8,options.multiplicity.singleton,options.varType.int,"number of threads to use")
options.register('isData',True,options.multiplicity.singleton,options.varType.bool,"is this data (sets GT to data and lumi sections)")
options.parseArguments()

process.source = cms.Source("PoolSource",
                           fileNames = cms.untracked.vstring(options.inputFiles),  
                          )
if options.isData:
    import FWCore.PythonUtilities.LumiList as LumiList
    process.source.lumisToProcess = LumiList.LumiList(filename = 'EgammaUser/EgammaDAS2020/data/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt').getVLuminosityBlockRange()


process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
if options.isData:
    process.GlobalTag = GlobalTag(process.GlobalTag, '106X_dataRun2_v20', '')
else:
    process.GlobalTag = GlobalTag(process.GlobalTag, '106X_mc2017_realistic_v6', '')


process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet(
    reportEvery = cms.untracked.int32(5000),
    limit = cms.untracked.int32(10000000)
)
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents)
)

process.options = cms.untracked.PSet(
    numberOfStreams = cms.untracked.uint32(options.nrThreads),
    numberOfThreads = cms.untracked.uint32(options.nrThreads),
    wantSummary = cms.untracked.bool(True)
)

# single lepton selector
process.goodElectrons = cms.EDFilter("PATElectronRefSelector",
                                     src = cms.InputTag("slimmedElectrons"),
                                     cut = cms.string("pt > 15 && abs(superCluster().eta())<1.4442")
                                 )
 
## dilepton selectors
process.diElectrons = cms.EDProducer("CandViewShallowCloneCombiner",
                                      decay       = cms.string("goodElectrons goodElectrons"),
                                      checkCharge = cms.bool(False),
                                      cut         = cms.string("mass > 20")
                                  )
 
# dilepton counter
process.diElectronsFilter = cms.EDFilter("CandViewCountFilter",
                                         src = cms.InputTag("diElectrons"),
                                        minNumber = cms.uint32(1)
                                     )

from EgammaUser.EgammaPostRecoTools.EgammaPostRecoTools import setupEgammaPostRecoSeq
setupEgammaPostRecoSeq(process,
                       runVID=False, 
                       era='2017-UL')    

process.skimPath = cms.Path(process.goodElectrons * process.diElectrons *process.diElectronsFilter* process.egammaPostRecoSeq)

process.output = cms.OutputModule("PoolOutputModule",
                                  splitLevel = cms.untracked.int32(0),
                                  outputCommands = cms.untracked.vstring(
                                      "drop *",
                                      "keep *_slimmedElectrons_*_*",
                                      "keep *_slimmedPhotons_*_*",
                                      "keep *_reducedEgamma_*_*",
                                      "keep *_slimmedPatTrigger_*_*",
                                      "keep *_packedGenParticles_*_*",
                                      "keep *_fixedGrid*_*_*",
                                      "keep *_TriggerResults_*_*",
                                      "keep *_offlineSlimmedPrimaryVertices_*_*",
                                      "keep *_slimmedPatTrigger_*_*"),
                                  fileName = cms.untracked.string(options.outputFile),
                                  SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('skimPath')),                                     
)

process.outPath = cms.EndPath(process.output)
