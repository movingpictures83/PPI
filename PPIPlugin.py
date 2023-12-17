import os
import pickle
import pandas as pd

import PyPluMA
import PyIO

class PPIPlugin:
    def input(self, inputfile):
       self.parameters = PyIO.readParameters(inputfile)
    def run(self):
       pass
    def output(self, outfile):
       inputfile = open(PyPluMA.prefix()+"/"+self.parameters["pickle"], 'rb')
       output = pickle.load(inputfile)

       scores_df = pd.read_csv(PyPluMA.prefix()+"/"+self.parameters["csvfile"])
       #scores_df = pd.read_csv("./data/masif_test/capri_quality_masif_test.csv")

       GRID_DIR = PyPluMA.prefix()+"/"+self.parameters["grid"]#'data/masif_test/prepare_energies_16R/07-grid/'
       ppi_list = os.listdir(GRID_DIR)
       ppi_list = [x.split('.npy')[0] for x in ppi_list if 'resnames' not in x and '.ref' not in x]
       all_ppis = ppi_list


       piston_score_df = pd.DataFrame({"PIsToN_score": output.cpu(), "PPI": all_ppis})
       scores_df = scores_df.merge(piston_score_df, how='left', on="PPI")

       scores_df

       scores_df['PID'] = scores_df['PPI'].apply(lambda x: x.split("-")[0])
       scores_df.to_csv(outfile.replace(".txt", ".ppi.csv"))

       ppi_list = [x.strip('\n') for x in open(PyPluMA.prefix()+"/"+self.parameters["original"])]
       #'./data/lists/masif_test_original.txt')]
       pid_list = [x.split('_')[0] for x in ppi_list if x.split('_')[0] in list(scores_df['PID'])]
       ppi_list = [x for x in ppi_list if x.split('_')[0] in pid_list]
       print(len(ppi_list))
       outputfile = open(outfile, 'w')
       for ppi in ppi_list:
          outputfile.write(ppi+"\n")
       print(len(ppi_list))

