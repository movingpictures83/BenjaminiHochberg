from scipy.stats import spearmanr
import pandas as pd
from statsmodels.stats.multitest import multipletests
import numpy as np


def correct_p_val(sp_df, p_df, to_file="False", method="bonferroni"):
    # Returns Spearman correlation filtered by Bonferroni correction
    p_corrected_df = p_df.apply(lambda x: multipletests(x, method=method, alpha=0.05)[0])
    #p_corrected_df = p_df
    sp_corrected = sp_df.where(p_corrected_df, other=0)
    print("We selected {} p_values".format(p_corrected_df.values.sum() - len(p_corrected_df)))

    if to_file!="False":
        sp_corrected.to_csv(to_file, index=True)
    return sp_corrected

def add_quote(in_file, out_file):
    i=0
    with open(in_file, "r") as in_f:
        with open(out_file, "w") as out_f:
            for line in in_f.readlines():
                if i==0:
                    line=line.strip("\n")
                    columns = line.split(",")
                    out_line = ""
                    for col in columns:
                        if '"' not in col:
                            out_line += '"' + col + '",'
                        else:
                            out_line += col + ","
                    out_line = out_line.strip(',')
                    out_line+="\n"
                else:
                    line = line.strip("\n")
                    columns = line.split(",")
                    out_line = ""
                    for j, col in enumerate(columns):
                        if j==0:
                            out_line += '"' + col + '",'
                        else:
                            out_line += col + ','
                    out_line = out_line.strip(',')
                    out_line += "\n"
                out_f.write(out_line)
                i+=1


# difCorr = "/Users/stebliankin/Desktop/MASH-CohortProject/Co-Occurrence/PLUMA-corrected/diffCorr.csv"
# pval = "/Users/stebliankin/Desktop/MASH-CohortProject/Co-Occurrence/PLUMA-corrected/diffPval.csv"
#
# outCorr = "/Users/stebliankin/Desktop/MASH-CohortProject/Co-Occurrence/PLUMA-corrected/diffCorr_correctedTMP.csv"
# outCorrFinal = "/Users/stebliankin/Desktop/MASH-CohortProject/Co-Occurrence/PLUMA-corrected/diffCorr_corrected.csv"

import PyIO
import PyPluMA

class BenjaminiHochbergPlugin:
    def input(self, inputfile):
        self.parameters = PyIO.readParameters(inputfile)
        self.difCorr = PyPluMA.prefix()+"/"+self.parameters["difCorr"]
        self.pval = PyPluMA.prefix()+"/"+self.parameters["pval"]
    def run(self):
        pass
    def output(self, outputfile):
        outCorr = outputfile+"TMP.csv"
        outCorrFinal = outputfile+".csv"
        sp_df, p_df = pd.read_csv(self.difCorr, index_col=0), pd.read_csv(self.pval, index_col=0)

        correctedDiffCorr = correct_p_val(sp_df, p_df, to_file=outCorr, method="fdr_bh")
        add_quote(outCorr, outCorrFinal)
