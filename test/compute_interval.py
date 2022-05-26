from PrepareDataframe import *
from GetHistoInfo import *
# Enable multi-threading
ROOT.EnableImplicitMT()
#ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(1111)

df = ROOT.RDataFrame("Events", "GluGluToRadionToHHTo2B2Tau_M-400.root")

#def GetMPV(df, drawHisto = False ):
def findMPV(df):
    df_eTau = DefineDataFrame(df, "eTau")
    df_muTau = DefineDataFrame(df, "muTau")
    df_tauTau = DefineDataFrame(df, "tauTau")

    df_eTau_2bGenJets = df_eTau.Define("GenJet_b_PF", "vec_i GenJet_b_PF; for(int i =0 ; i<GenJet_partonFlavour.size(); i++){if (std::abs(GenJet_partonFlavour[i])==5){GenJet_b_PF.push_back(i);}} return GenJet_b_PF;").Define("GenJet_b_PF_size", "GenJet_b_PF.size()").Filter("GenJet_b_PF_size==2").Define("Two_bGenJets_invMass", "InvMassByFalvour(GenJet_pt, GenJet_eta, GenJet_phi, GenJet_mass, GenJet_partonFlavour, true)")
    histo_eTau_2bGenJets = df_eTau_2bGenJets.Histo1D(("Two_bGenJets_invMass_eTau", "Two_bGenJets_invMass_eTau", 400, -0.5, 199.5),"Two_bGenJets_invMass").GetValue()
    df_muTau_2bGenJets = df_muTau.Define("GenJet_b_PF", "vec_i GenJet_b_PF; for(int i =0 ; i<GenJet_partonFlavour.size(); i++){if (std::abs(GenJet_partonFlavour[i])==5){GenJet_b_PF.push_back(i);}} return GenJet_b_PF;").Define("GenJet_b_PF_size", "GenJet_b_PF.size()").Filter("GenJet_b_PF_size==2").Define("Two_bGenJets_invMass", "InvMassByFalvour(GenJet_pt, GenJet_eta, GenJet_phi, GenJet_mass, GenJet_partonFlavour, true)")
    histo_muTau_2bGenJets = df_muTau_2bGenJets.Histo1D(("Two_bGenJets_invMass_muTau", "Two_bGenJets_invMass_muTau", 400, -0.5, 199.5),"Two_bGenJets_invMass").GetValue()
    df_tauTau_2bGenJets = df_tauTau.Define("GenJet_b_PF", "vec_i GenJet_b_PF; for(int i =0 ; i<GenJet_partonFlavour.size(); i++){if (std::abs(GenJet_partonFlavour[i])==5){GenJet_b_PF.push_back(i);}} return GenJet_b_PF;").Define("GenJet_b_PF_size", "GenJet_b_PF.size()").Filter("GenJet_b_PF_size==2").Define("Two_bGenJets_invMass", "InvMassByFalvour(GenJet_pt, GenJet_eta, GenJet_phi, GenJet_mass, GenJet_partonFlavour, true)")
    histo_tauTau_2bGenJets = df_tauTau_2bGenJets.Histo1D(("Two_bGenJets_invMass_tauTau", "Two_bGenJets_invMass_tauTau", 400, -0.5, 199.5),"Two_bGenJets_invMass").GetValue()

    histo_tot = ROOT.TH1D(histo_eTau_2bGenJets)
    histo_tot.Add(histo_tot,histo_muTau_2bGenJets)
    histo_tot.Add(histo_tot,histo_tauTau_2bGenJets)
    #if(drawHisto):
    #    histo_tot_canvas = ROOT.TCanvas()
    #    histo_tot_canvas.cd()
    #    histo_tot.Draw()
    #    histo_tot_canvas.Update()
    #    input()

    #print(histo_tot.GetBinWidth(2))
    y_max = histo_tot.GetMaximumBin()
    x_max = histo_tot.GetXaxis().GetBinCenter(y_max)
    return x_max
#print(y_max, x_max)
#return x_max

def EvaluateDiffInt(array):
    step = 0.001
    q = np.arange(0, 1 + step, step)
    x_q = np.quantile(array, step)

    interval = 0.68
    quantiles=[]
    differences =[]
    diff_quantiles =[]
    for i in q:
        for j in q:
            if((i-j)==0.68):
                differences.append([j, i])
                quantiles.append([np.quantile(array, j),np.quantile(array, i)])
                diff_quantiles.append(np.quantile(array, i)-np.quantile(array, j))
    #print(quantiles, differences, diff_quantiles)
    minimum=min(diff_quantiles)
    min_index= diff_quantiles.index(minimum)
    min_diff = differences[min_index ]
    min_quantiles= quantiles[min_index  ]
    #print(f"min_index = {min_index}, minimum = {minimum}, min_diff = {min_diff}, min_quantiles = {min_quantiles} ")

    return min_index, minimum, min_diff, min_quantiles

'''
print("for events with only 2 b-jets")
npy_eTau = df_eTau_2bGenJets.AsNumpy(columns=["Two_bGenJets_invMass"])
min_index_eTau, minimum_eTau, min_diff_eTau, min_quantiles_eTau = EvaluateDiffInt(npy_eTau["Two_bGenJets_invMass"])
print(f"min_index eTau = {min_index_eTau}, minimum eTau = {minimum_eTau}, min_diff eTau = {min_diff_eTau}, min_quantiles eTau = {min_quantiles_eTau} ")

npy_muTau = df_muTau_2bGenJets.AsNumpy(columns=["Two_bGenJets_invMass"])
min_index_muTau, minimum_muTau, min_diff_muTau, min_quantiles_muTau = EvaluateDiffInt(npy_muTau["Two_bGenJets_invMass"])
print(f"min_index muTau = {min_index_muTau}, minimum muTau = {minimum_muTau}, min_diff muTau = {min_diff_muTau}, min_quantiles muTau = {min_quantiles_muTau} ")

npy_tauTau = df_tauTau_2bGenJets.AsNumpy(columns=["Two_bGenJets_invMass"])
min_index_tauTau, minimum_tauTau, min_diff_tauTau, min_quantiles_tauTau = EvaluateDiffInt(npy_tauTau["Two_bGenJets_invMass"])
print(f"min_index tauTau = {min_index_tauTau}, minimum tauTau = {minimum_tauTau}, min_diff tauTau = {min_diff_tauTau}, min_quantiles tauTau = {min_quantiles_tauTau} ")

print("for events with >2 b-jets ")
df_eTau_Greater2_GenJets_b = df_eTau.Define("GenJet_b_PF", "vec_i GenJet_b_PF; for(int i =0 ; i<GenJet_partonFlavour.size(); i++){if (std::abs(GenJet_partonFlavour[i])==5){GenJet_b_PF.push_back(i);}} return GenJet_b_PF;").Define("GenJet_b_PF_size", "GenJet_b_PF.size()").Filter("GenJet_b_PF_size>2")
df_muTau_Greater2_GenJets_b = df_muTau.Define("GenJet_b_PF", "vec_i GenJet_b_PF; for(int i =0 ; i<GenJet_partonFlavour.size(); i++){if (std::abs(GenJet_partonFlavour[i])==5){GenJet_b_PF.push_back(i);}} return GenJet_b_PF;").Define("GenJet_b_PF_size", "GenJet_b_PF.size()").Filter("GenJet_b_PF_size>2")
df_tauTau_Greater2_GenJets_b = df_tauTau.Define("GenJet_b_PF", "vec_i GenJet_b_PF; for(int i =0 ; i<GenJet_partonFlavour.size(); i++){if (std::abs(GenJet_partonFlavour[i])==5){GenJet_b_PF.push_back(i);}} return GenJet_b_PF;").Define("GenJet_b_PF_size", "GenJet_b_PF.size()").Filter("GenJet_b_PF_size>2")

print("\nevaluating invMass of 2 mostEnergetic b-jets")

df_eTau_Greater2_GenJets_b_2MostEnergeticsMass= df_eTau_Greater2_GenJets_b.Define("ReorderedJetsInPt", "ReorderJets(GenJet_pt, GenJet_b_PF)").Define("two_most_energetic_bGenJets", "vec_i twoMostEnergeticJets; for(int i = 0; i<2; i++){twoMostEnergeticJets.push_back(ReorderedJetsInPt[i]);}  return twoMostEnergeticJets;").Define("Two_MostEnergetic_bGenJets_invMass", "InvMassByIndices(two_most_energetic_bGenJets,GenJet_pt, GenJet_eta, GenJet_phi, GenJet_mass,GenJet_partonFlavour, true)")
df_muTau_Greater2_GenJets_b_2MostEnergeticsMass= df_muTau_Greater2_GenJets_b.Define("ReorderedJetsInPt", "ReorderJets(GenJet_pt, GenJet_b_PF)").Define("two_most_energetic_bGenJets", "vec_i twoMostEnergeticJets; for(int i = 0; i<2; i++){twoMostEnergeticJets.push_back(ReorderedJetsInPt[i]);}  return twoMostEnergeticJets;").Define("Two_MostEnergetic_bGenJets_invMass", "InvMassByIndices(two_most_energetic_bGenJets,GenJet_pt, GenJet_eta, GenJet_phi, GenJet_mass,GenJet_partonFlavour, true)")
df_tauTau_Greater2_GenJets_b_2MostEnergeticsMass= df_tauTau_Greater2_GenJets_b.Define("ReorderedJetsInPt", "ReorderJets(GenJet_pt, GenJet_b_PF)").Define("two_most_energetic_bGenJets", "vec_i twoMostEnergeticJets; for(int i = 0; i<2; i++){twoMostEnergeticJets.push_back(ReorderedJetsInPt[i]);}  return twoMostEnergeticJets;").Define("Two_MostEnergetic_bGenJets_invMass", "InvMassByIndices(two_most_energetic_bGenJets,GenJet_pt, GenJet_eta, GenJet_phi, GenJet_mass,GenJet_partonFlavour, true)")

npy_eTau_Greater2_GenJets_b_2MostEnergeticsMass = df_eTau_Greater2_GenJets_b_2MostEnergeticsMass.AsNumpy(columns=["Two_MostEnergetic_bGenJets_invMass"])
min_index_eTau_Greater2_GenJets_b_2MostEnergeticsMass, minimum_eTau_Greater2_GenJets_b_2MostEnergeticsMass, min_diff_eTau_Greater2_GenJets_b_2MostEnergeticsMass, min_quantiles_eTau_Greater2_GenJets_b_2MostEnergeticsMass = EvaluateDiffInt(npy_eTau_Greater2_GenJets_b_2MostEnergeticsMass["Two_MostEnergetic_bGenJets_invMass"])
print(f"min_index eTau = {min_index_eTau_Greater2_GenJets_b_2MostEnergeticsMass}, minimum eTau = {minimum_eTau_Greater2_GenJets_b_2MostEnergeticsMass}, min_diff eTau = {min_diff_eTau_Greater2_GenJets_b_2MostEnergeticsMass}, min_quantiles eTau = {min_quantiles_eTau_Greater2_GenJets_b_2MostEnergeticsMass} ")

npy_muTau_Greater2_GenJets_b_2MostEnergeticsMass = df_muTau_Greater2_GenJets_b_2MostEnergeticsMass.AsNumpy(columns=["Two_MostEnergetic_bGenJets_invMass"])
min_index_muTau_Greater2_GenJets_b_2MostEnergeticsMass, minimum_muTau_Greater2_GenJets_b_2MostEnergeticsMass, min_diff_muTau_Greater2_GenJets_b_2MostEnergeticsMass, min_quantiles_muTau_Greater2_GenJets_b_2MostEnergeticsMass = EvaluateDiffInt(npy_muTau_Greater2_GenJets_b_2MostEnergeticsMass["Two_MostEnergetic_bGenJets_invMass"])
print(f"min_index muTau = {min_index_muTau_Greater2_GenJets_b_2MostEnergeticsMass}, minimum muTau = {minimum_muTau_Greater2_GenJets_b_2MostEnergeticsMass}, min_diff muTau = {min_diff_muTau_Greater2_GenJets_b_2MostEnergeticsMass}, min_quantiles muTau = {min_quantiles_muTau_Greater2_GenJets_b_2MostEnergeticsMass} ")

npy_tauTau_Greater2_GenJets_b_2MostEnergeticsMass = df_tauTau_Greater2_GenJets_b_2MostEnergeticsMass.AsNumpy(columns=["Two_MostEnergetic_bGenJets_invMass"])
min_index_tauTau_Greater2_GenJets_b_2MostEnergeticsMass, minimum_tauTau_Greater2_GenJets_b_2MostEnergeticsMass, min_diff_tauTau_Greater2_GenJets_b_2MostEnergeticsMass, min_quantiles_tauTau_Greater2_GenJets_b_2MostEnergeticsMass = EvaluateDiffInt(npy_tauTau_Greater2_GenJets_b_2MostEnergeticsMass["Two_MostEnergetic_bGenJets_invMass"])
print(f"min_index tauTau = {min_index_tauTau_Greater2_GenJets_b_2MostEnergeticsMass}, minimum tauTau = {minimum_tauTau_Greater2_GenJets_b_2MostEnergeticsMass}, min_diff tauTau = {min_diff_tauTau_Greater2_GenJets_b_2MostEnergeticsMass}, min_quantiles tauTau = {min_quantiles_tauTau_Greater2_GenJets_b_2MostEnergeticsMass} ")

print("\nevaluating invMass of all b-jets in the event")
df_eTau_Greater2_GenJets_b_allMass= df_eTau_Greater2_GenJets_b.Define("all_bGenJets_invMass", "InvMassByFalvour(GenJet_pt, GenJet_eta, GenJet_phi, GenJet_mass, GenJet_partonFlavour, true)")
df_muTau_Greater2_GenJets_b_allMass= df_muTau_Greater2_GenJets_b.Define("all_bGenJets_invMass", "InvMassByFalvour(GenJet_pt, GenJet_eta, GenJet_phi, GenJet_mass, GenJet_partonFlavour, true)")
df_tauTau_Greater2_GenJets_b_allMass= df_tauTau_Greater2_GenJets_b.Define("all_bGenJets_invMass", "InvMassByFalvour(GenJet_pt, GenJet_eta, GenJet_phi, GenJet_mass, GenJet_partonFlavour, true)")

npy_eTau_Greater2_GenJets_b_allMass = df_eTau_Greater2_GenJets_b_allMass.AsNumpy(columns=["all_bGenJets_invMass"])
min_index_eTau_Greater2_GenJets_b_allMass, minimum_eTau_Greater2_GenJets_b_allMass, min_diff_eTau_Greater2_GenJets_b_allMass, min_quantiles_eTau_Greater2_GenJets_b_allMass = EvaluateDiffInt(npy_eTau_Greater2_GenJets_b_allMass["all_bGenJets_invMass"])
print(f"min_index eTau = {min_index_eTau_Greater2_GenJets_b_allMass}, minimum eTau = {minimum_eTau_Greater2_GenJets_b_allMass}, min_diff eTau = {min_diff_eTau_Greater2_GenJets_b_allMass}, min_quantiles eTau = {min_quantiles_eTau_Greater2_GenJets_b_allMass} ")

npy_muTau_Greater2_GenJets_b_allMass = df_muTau_Greater2_GenJets_b_allMass.AsNumpy(columns=["all_bGenJets_invMass"])
min_index_muTau_Greater2_GenJets_b_allMass, minimum_muTau_Greater2_GenJets_b_allMass, min_diff_muTau_Greater2_GenJets_b_allMass, min_quantiles_muTau_Greater2_GenJets_b_allMass = EvaluateDiffInt(npy_muTau_Greater2_GenJets_b_allMass["all_bGenJets_invMass"])
print(f"min_index muTau = {min_index_muTau_Greater2_GenJets_b_allMass}, minimum muTau = {minimum_muTau_Greater2_GenJets_b_allMass}, min_diff muTau = {min_diff_muTau_Greater2_GenJets_b_allMass}, min_quantiles muTau = {min_quantiles_muTau_Greater2_GenJets_b_allMass} ")

npy_tauTau_Greater2_GenJets_b_allMass = df_tauTau_Greater2_GenJets_b_allMass.AsNumpy(columns=["all_bGenJets_invMass"])
min_index_tauTau_Greater2_GenJets_b_allMass, minimum_tauTau_Greater2_GenJets_b_allMass, min_diff_tauTau_Greater2_GenJets_b_allMass, min_quantiles_tauTau_Greater2_GenJets_b_allMass = EvaluateDiffInt(npy_tauTau_Greater2_GenJets_b_allMass["all_bGenJets_invMass"])
print(f"min_index tauTau = {min_index_tauTau_Greater2_GenJets_b_allMass}, minimum tauTau = {minimum_tauTau_Greater2_GenJets_b_allMass}, min_diff tauTau = {min_diff_tauTau_Greater2_GenJets_b_allMass}, min_quantiles tauTau = {min_quantiles_tauTau_Greater2_GenJets_b_allMass} ")

print(f"\nevaluating invMass of the two b-jets closest to the mpv {x_max}")

df_eTau_Greater2_GenJets_b_2ClosestToMPVMass= df_eTau_Greater2_GenJets_b.Define("TwobJetsClosestToMPV", f"(FindTwoJetsClosestToMPV({x_max},GenJet_pt, GenJet_eta, GenJet_phi, GenJet_mass, GenJet_partonFlavour))").Define("Two_ClosestToMPV_bGenJets_invMass", "InvMassByIndices(TwobJetsClosestToMPV,GenJet_pt, GenJet_eta, GenJet_phi, GenJet_mass,GenJet_partonFlavour, true)")
df_muTau_Greater2_GenJets_b_2ClosestToMPVMass= df_muTau_Greater2_GenJets_b.Define("TwobJetsClosestToMPV", f"(FindTwoJetsClosestToMPV({x_max},GenJet_pt, GenJet_eta, GenJet_phi, GenJet_mass, GenJet_partonFlavour))").Define("Two_ClosestToMPV_bGenJets_invMass", "InvMassByIndices(TwobJetsClosestToMPV,GenJet_pt, GenJet_eta, GenJet_phi, GenJet_mass,GenJet_partonFlavour, true)")
df_tauTau_Greater2_GenJets_b_2ClosestToMPVMass= df_tauTau_Greater2_GenJets_b.Define("TwobJetsClosestToMPV", f"(FindTwoJetsClosestToMPV({x_max},GenJet_pt, GenJet_eta, GenJet_phi, GenJet_mass, GenJet_partonFlavour))").Define("Two_ClosestToMPV_bGenJets_invMass", "InvMassByIndices(TwobJetsClosestToMPV,GenJet_pt, GenJet_eta, GenJet_phi, GenJet_mass,GenJet_partonFlavour, true)")

npy_eTau_Greater2_GenJets_b_2ClosestToMPVMass = df_eTau_Greater2_GenJets_b_2ClosestToMPVMass.AsNumpy(columns=["Two_ClosestToMPV_bGenJets_invMass"])
min_index_eTau_Greater2_GenJets_b_2ClosestToMPVMass, minimum_eTau_Greater2_GenJets_b_2ClosestToMPVMass, min_diff_eTau_Greater2_GenJets_b_2ClosestToMPVMass, min_quantiles_eTau_Greater2_GenJets_b_2ClosestToMPVMass = EvaluateDiffInt(npy_eTau_Greater2_GenJets_b_2ClosestToMPVMass["Two_ClosestToMPV_bGenJets_invMass"])
print(f"min_index eTau = {min_index_eTau_Greater2_GenJets_b_2ClosestToMPVMass}, minimum eTau = {minimum_eTau_Greater2_GenJets_b_2ClosestToMPVMass}, min_diff eTau = {min_diff_eTau_Greater2_GenJets_b_2ClosestToMPVMass}, min_quantiles eTau = {min_quantiles_eTau_Greater2_GenJets_b_2ClosestToMPVMass} ")

npy_muTau_Greater2_GenJets_b_2ClosestToMPVMass = df_muTau_Greater2_GenJets_b_2ClosestToMPVMass.AsNumpy(columns=["Two_ClosestToMPV_bGenJets_invMass"])
min_index_muTau_Greater2_GenJets_b_2ClosestToMPVMass, minimum_muTau_Greater2_GenJets_b_2ClosestToMPVMass, min_diff_muTau_Greater2_GenJets_b_2ClosestToMPVMass, min_quantiles_muTau_Greater2_GenJets_b_2ClosestToMPVMass = EvaluateDiffInt(npy_muTau_Greater2_GenJets_b_2ClosestToMPVMass["Two_ClosestToMPV_bGenJets_invMass"])
print(f"min_index muTau = {min_index_muTau_Greater2_GenJets_b_2ClosestToMPVMass}, minimum muTau = {minimum_muTau_Greater2_GenJets_b_2ClosestToMPVMass}, min_diff muTau = {min_diff_muTau_Greater2_GenJets_b_2ClosestToMPVMass}, min_quantiles muTau = {min_quantiles_muTau_Greater2_GenJets_b_2ClosestToMPVMass} ")

npy_tauTau_Greater2_GenJets_b_2ClosestToMPVMass = df_tauTau_Greater2_GenJets_b_2ClosestToMPVMass.AsNumpy(columns=["Two_ClosestToMPV_bGenJets_invMass"])
min_index_tauTau_Greater2_GenJets_b_2ClosestToMPVMass, minimum_tauTau_Greater2_GenJets_b_2ClosestToMPVMass, min_diff_tauTau_Greater2_GenJets_b_2ClosestToMPVMass, min_quantiles_tauTau_Greater2_GenJets_b_2ClosestToMPVMass = EvaluateDiffInt(npy_tauTau_Greater2_GenJets_b_2ClosestToMPVMass["Two_ClosestToMPV_bGenJets_invMass"])
print(f"min_index tauTau = {min_index_tauTau_Greater2_GenJets_b_2ClosestToMPVMass}, minimum tauTau = {minimum_tauTau_Greater2_GenJets_b_2ClosestToMPVMass}, min_diff tauTau = {min_diff_tauTau_Greater2_GenJets_b_2ClosestToMPVMass}, min_quantiles tauTau = {min_quantiles_tauTau_Greater2_GenJets_b_2ClosestToMPVMass} ")
''
all_differences_eTau = []
all_differences_muTau = []
all_differences_tauTau = []
all_differences_idx = ["2 Most energetic"," all ","2 closest to MPV"]

diff_min_quantiles_eTau_Greater2_GenJets_b_2MostEnergeticsMass = min_quantiles_eTau_Greater2_GenJets_b_2MostEnergeticsMass[1]-min_quantiles_eTau_Greater2_GenJets_b_2MostEnergeticsMass[0]

diff_min_quantiles_muTau_Greater2_GenJets_b_2MostEnergeticsMass = min_quantiles_muTau_Greater2_GenJets_b_2MostEnergeticsMass[1]-min_quantiles_muTau_Greater2_GenJets_b_2MostEnergeticsMass[0]

diff_min_quantiles_tauTau_Greater2_GenJets_b_2MostEnergeticsMass = min_quantiles_tauTau_Greater2_GenJets_b_2MostEnergeticsMass[1]-min_quantiles_tauTau_Greater2_GenJets_b_2MostEnergeticsMass[0]

diff_min_quantiles_eTau_Greater2_GenJets_b_allMass = min_quantiles_eTau_Greater2_GenJets_b_allMass[1]-min_quantiles_eTau_Greater2_GenJets_b_allMass[0]

diff_min_quantiles_muTau_Greater2_GenJets_b_allMass = min_quantiles_muTau_Greater2_GenJets_b_allMass[1]-min_quantiles_muTau_Greater2_GenJets_b_allMass[0]

diff_min_quantiles_tauTau_Greater2_GenJets_b_allMass = min_quantiles_tauTau_Greater2_GenJets_b_allMass[1]-min_quantiles_tauTau_Greater2_GenJets_b_allMass[0]

diff_min_quantiles_eTau_Greater2_GenJets_b_2ClosestToMPVMass = min_quantiles_eTau_Greater2_GenJets_b_2ClosestToMPVMass[1]-min_quantiles_eTau_Greater2_GenJets_b_2ClosestToMPVMass[0]

diff_min_quantiles_muTau_Greater2_GenJets_b_2ClosestToMPVMass = min_quantiles_muTau_Greater2_GenJets_b_2ClosestToMPVMass[1]-min_quantiles_muTau_Greater2_GenJets_b_2ClosestToMPVMass[0]

diff_min_quantiles_tauTau_Greater2_GenJets_b_2ClosestToMPVMass = min_quantiles_tauTau_Greater2_GenJets_b_2ClosestToMPVMass[1]-min_quantiles_tauTau_Greater2_GenJets_b_2ClosestToMPVMass[0]

all_differences_eTau.append(diff_min_quantiles_eTau_Greater2_GenJets_b_2MostEnergeticsMass)
all_differences_eTau.append(diff_min_quantiles_eTau_Greater2_GenJets_b_allMass)
all_differences_eTau.append(diff_min_quantiles_eTau_Greater2_GenJets_b_2ClosestToMPVMass )

all_differences_muTau.append(diff_min_quantiles_muTau_Greater2_GenJets_b_2MostEnergeticsMass)
all_differences_muTau.append(diff_min_quantiles_muTau_Greater2_GenJets_b_allMass)
all_differences_muTau.append(diff_min_quantiles_muTau_Greater2_GenJets_b_2ClosestToMPVMass )

all_differences_tauTau.append(diff_min_quantiles_tauTau_Greater2_GenJets_b_2MostEnergeticsMass)
all_differences_tauTau.append(diff_min_quantiles_tauTau_Greater2_GenJets_b_allMass)
all_differences_tauTau.append(diff_min_quantiles_tauTau_Greater2_GenJets_b_2ClosestToMPVMass )
print()
min_eTau = min(all_differences_eTau)
print(f"for eTau, the minimum is {min_eTau}, for {all_differences_idx[all_differences_eTau.index(min_eTau)]}")
min_muTau= min(all_differences_muTau)
print(f"for muTau, the minimum is {min_muTau}, for {all_differences_idx[all_differences_muTau.index(min_muTau)]}")
min_tauTau = min(all_differences_tauTau)
print(f"for tauTau, the minimum is {min_tauTau}, for {all_differences_idx[all_differences_tauTau.index(min_tauTau)]}")
'''
