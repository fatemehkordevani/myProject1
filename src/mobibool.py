# this file is supposed to get mobidb+mutposition, is_in_startend and ndd bool, index*, and give a df in the outcome
# with added columns: brain bool, ASD bool, EE bool, ID bool, SCZ bool
# *index (mutual idx of mut_acc_merged_df and mutinfo subdf which is useful to merge mobidb & g4dn_mutinfo_acc,
# could be useless now :/ not sure

import pandas as pd
import numpy as np
from pandas import DataFrame
import config as cfg
import sys
import brain as bd

if __name__ == '__main__':
    # this file is generated in categorizer.py with mobi_mut_inidr_checker()
    mobi_ndd_idr_df = pd.read_csv(cfg.data['gene4'] + '/mut-pos-mobi100.csv', low_memory=False)
    mobi_ndd_idr_df = mobi_ndd_idr_df.drop(['Unnamed: 0', 'index', 'position', 'Length', 'is_in_startend'], axis=1)
    mobi_ndd_idr_df = mobi_ndd_idr_df.drop_duplicates()
    ## brain proteins
    brain_prot_lst = bd.brain_pr_lst_generator()  # n: 8428
    brain_pr_df = DataFrame(brain_prot_lst, columns=['brain_acc'])
    brain_pr_df = brain_pr_df.dropna()  # 8337
    brain_pr_df['brain'] = 1
    mobi_brain_bool_df = pd.concat([mobi_ndd_idr_df, brain_pr_df], axis=1)
    mobi_brain_bool_df['brain'] = mobi_brain_bool_df['brain'].fillna(0)
    mobi_brain_bool_df = mobi_brain_bool_df.drop(['brain_acc'], axis=1)  # (1212280, 12)

    ## Phenotypes
    mobi_bool_df = mobi_brain_bool_df
    mobi_bool_df['ASD'] = np.where(mobi_bool_df['Phenotype'] == 'ASD', 1, 0)
    mobi_bool_df['EE'] = np.where(mobi_bool_df['Phenotype'] == 'EE', 1, 0)
    mobi_bool_df['SCZ'] = np.where(mobi_bool_df['Phenotype'] == 'SCZ', 1, 0)
    mobi_bool_df['ID'] = np.where(mobi_bool_df['Phenotype'] == 'ID', 1, 0)

    positive_cand_g4mobi_df = pd.read_csv(cfg.data['gene4'] + '/positive_cand_g4mobi_concat.csv')

    sys.exit()
