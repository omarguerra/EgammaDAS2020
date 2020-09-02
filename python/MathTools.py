#so normally I would not roll my own DR function (too many buggy dr functions already exist in this world)
#however in the CMSDAS release ROOT.reco.calDeltaR2 which I normally use (the CMSSW DR function)
#can not be accessed for some werid reason, sigh
import math

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

